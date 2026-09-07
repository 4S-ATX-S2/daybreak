#!/usr/bin/env python3
"""
daybreak — the Daybreak Brief pipeline.

    daybreak fetch    --date 2026-09-07 [--double-read] [--rows 1,4,20]
    daybreak gates    --date 2026-09-07
    daybreak draft    --date 2026-09-07          (the only stage that needs a model)
    daybreak build    --date 2026-09-07
    daybreak publish  --date 2026-09-07
    daybreak status

Four stages, run independently on purpose.

    DEGRADED MODE: if `draft` cannot run — no license, outage, a deputy at 4 AM —
    then `fetch` + `build` still produce a facts-only brief: weather table, watch-item
    ages, events, chips carried forward unchanged, no prose. Ugly, true, on time.
    That is a far better failure than nothing.

Standard library only. No pip install.
"""

import argparse, json, os, subprocess, sys, time
from datetime import datetime, date as _date
from pathlib import Path

HERE = Path(__file__).resolve().parent
import collectors, gates                                     # noqa: E402

OUT   = HERE / "out"
RAW   = HERE / "raw"
STATE = HERE / "state"
for d in (OUT, RAW, STATE):
    d.mkdir(exist_ok=True)

C = {"g": "\033[32m", "r": "\033[31m", "y": "\033[33m", "b": "\033[1m", "x": "\033[0m"}
if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
    C = {k: "" for k in C}


def load_sources():
    return json.loads((HERE / "sources.json").read_text())


def edition_for(d):
    """Ed. 250 == 2026-09-06. The number is a fact about the date, not a guess."""
    return 250 + (_date.fromisoformat(d) - _date(2026, 9, 6)).days


def paths(d):
    return {"facts": OUT / f"facts_{d}.json", "gates": OUT / f"gates_{d}.json",
            "raw": RAW / d, "brief": OUT / f"brief_{d}.md"}


def browser_fallback(row):
    """A row that declares fallback:browser gets one Chromium attempt before it is
    called dead. Bot walls (texassports, the Hormuz tracker) serve a real browser."""
    js = HERE / "browserfetch.js"
    url = row.get("args", {}).get("url")
    if not js.exists() or not url:
        return None
    try:
        pr = subprocess.run(["node", str(js), url], capture_output=True, text=True, timeout=70)
    except Exception as e:
        return None
    if pr.returncode == 0 and pr.stdout.strip():
        return {"id": row["id"], "url": url, "ok": True,
                "fetched_at": datetime.now().astimezone().isoformat(),
                "via": "browser fallback",
                "raw": pr.stdout, "data": {"text_excerpt": pr.stdout[:6000],
                                           "bytes": len(pr.stdout)}, "error": None}
    return None


# --------------------------------------------------------------------- fetch --

def cmd_fetch(a):
    src = load_sources()
    ua, cfg = src["user_agent"], src["point"]
    rows = src["tier1"]
    if a.rows:
        want = {int(x) for x in a.rows.split(",")}
        rows = [r for r in rows if r["n"] in want]

    p = paths(a.date)
    p["raw"].mkdir(exist_ok=True)
    print(f"{C['b']}daybreak fetch{C['x']}  {a.date}  ed. {edition_for(a.date)}  "
          f"{len(rows)} rows\n")

    results = []
    for row in rows:
        t0 = time.time()
        r = collectors.run_row(row, cfg, ua)
        if (not r["ok"]) and row.get("fallback") == "browser":
            r2 = browser_fallback(row)
            if r2:
                r = r2
        dt = time.time() - t0
        mark = f"{C['g']}ok  {C['x']}" if r["ok"] else f"{C['r']}DEAD{C['x']}"
        detail = "" if r["ok"] else f"  <- {r['error']}"
        if r["ok"] and r.get("via"):
            mark = f"{C['y']}ok* {C['x']}"
            detail = "  <- via browser fallback"
        elif (not r["ok"]) and row.get("fallback"):
            detail += f"  {C['r']}[FALLBACK ALSO FAILED — FETCH THIS ROW BY HAND]{C['x']}"
            r["needs_manual"] = True
        print(f"  {mark} {row['n']:>2}. {row['name'][:46]:<46} {dt:5.1f}s{detail}")
        if r.get("raw"):
            (p["raw"] / f"{row['id']}.txt").write_text(r["raw"][:400_000])
        r.pop("raw", None)
        r["row"] = {"n": row["n"], "name": row["name"], "rule": row.get("rule", "")}
        results.append(r)

    # --- G14 second read of the worded forecast -----------------------------
    prior = None
    fc = next((r for r in results if r["id"] == "nws_point_forecast" and r["ok"]), None)
    if fc:
        last = STATE / "last_forecast.json"
        if last.exists():
            prior = json.loads(last.read_text())
        if a.double_read:
            print(f"\n  {C['y']}G14{C['x']} second read in {a.reread_delay}s …")
            time.sleep(a.reread_delay)
            again = collectors.run_row(
                next(r for r in src["tier1"] if r["id"] == "nws_point_forecast"), cfg, ua)
            if again["ok"]:
                prior = fc["data"]                 # compare new vs the read we just took
                fc = again
                fc.pop("raw", None)
                fc["row"] = {"n": 1, "name": "NWS point forecast", "rule": "double-read"}
                results = [fc if r["id"] == "nws_point_forecast" else r for r in results]
        last.write_text(json.dumps(fc["data"], indent=2))

    # A partial run (--rows) MERGES into the day's facts. It must never silently
    # replace 23 rows with 2 — that would hand the draft stage a false G13 pass.
    merged = results
    if p["facts"].exists():
        prev = json.loads(p["facts"].read_text()).get("results", [])
        fresh = {r["id"] for r in results}
        merged = results + [r for r in prev if r["id"] not in fresh]
        merged.sort(key=lambda r: r.get("row", {}).get("n", 99))
    facts = {
        "date": a.date, "edition": edition_for(a.date),
        "generated_at": datetime.now().astimezone().isoformat(),
        "manifest_version": src["version"],
        "results": merged,
    }
    p["facts"].write_text(json.dumps(facts, indent=2))

    # --- gates ---------------------------------------------------------------
    g13_status, g13_report = gates.g13(merged, src["tier1"], partial=bool(a.rows))
    g14_status, g14_report = ("N/A", {"gate": "G14", "status": "N/A — forecast row not fetched"})
    if fc:
        g14_status, g14_report = gates.g14(
            fc["data"].get("periods", []), (prior or {}).get("periods", []),
            src["thresholds"], src["threshold_margin"])

    p["gates"].write_text(json.dumps({"G13": g13_report, "G14": g14_report}, indent=2))
    print_gates(g13_report, g14_report)
    if g13_status == "PARTIAL":
        print(f"\n  {C['y']}PARTIAL RUN — not publishable. Re-run without --rows "
              f"before drafting an edition.{C['x']}")
    return 0 if g13_status != "FAIL" else 2


def print_gates(g13r, g14r):
    col = {"PASS": C["g"], "DEGRADED": C["y"], "FAIL": C["r"],
           "STRADDLE": C["y"]}.get(g13r["status"], "")
    print(f"\n{C['b']}── GATES ──{C['x']}")
    print(f"  G13 SOURCE COVERAGE  {col}{g13r['status']}{C['x']}"
          f"  ({g13r['attempted'] - len(g13r['unreachable'])}/{g13r['attempted']} reachable)")
    for u in g13r["unreachable"]:
        print(f"      {C['r']}·{C['x']} row {u['n']} {u['name']} — {u['error']}")
        print(f"        {C['y']}MUST APPEAR AS A PUBLISHED GAP.{C['x']} {u['rule'][:90]}")
    na = g13r.get("not_attempted", [])
    if na:
        nums = ",".join(str(x["n"]) for x in na[:12]) + ("…" if len(na) > 12 else "")
        word = "not run (deliberate subset)" if g13r["status"] == "PARTIAL" else \
               "NEVER ATTEMPTED — this build is broken"
        print(f"      {C['y']}·{C['x']} {len(na)} rows {word}: {nums}")
        print(f"        {g13r['publish_instruction']}")
    st = g14r.get("status", "N/A")
    col2 = C["r"] if str(st).startswith("STRADDLE") else C["g"]
    print(f"  G14 THRESHOLD RE-READ  {col2}{st}{C['x']}")
    for f in g14r.get("findings", []):
        icon = "⚠" if f["straddle"] else "·"
        print(f"      {icon} {f['period']}: {f['field']} {f['prior']} → {f['current']} "
              f"vs {f['criterion']} {f['threshold']}")
        print(f"        {f['verdict']}")


# --------------------------------------------------------------- other stages --

def cmd_gates(a):
    p = paths(a.date)
    if not p["gates"].exists():
        print(f"{C['r']}no gate report for {a.date} — run `daybreak fetch` first{C['x']}")
        return 2
    g = json.loads(p["gates"].read_text())
    print_gates(g["G13"], g["G14"])
    return 0


PROMPT = """You are producing ATX-DB-2026-{ed}, the Daybreak Brief for {date}.

READ FIRST, IN THIS ORDER:
  1. state/LATEST_STATE.md      — what the last edition carried forward
  2. 05_VERIFICATION_RULES.md   — 12 rules, each written from a real published error
  3. 03_HOUSE_STYLE.md          — voice, chips, flag bands
  4. out/facts_{date}.json      — everything fetched this run
  5. out/gates_{date}.json      — G13 and G14. THESE ARE NOT ADVISORY.

HARD CONSTRAINTS
  · Every UNREACHABLE row in G13 is published as "not verified this pass". Never estimated,
    never silently dropped. Silence is the only forbidden outcome.
  · Every STRADDLE in G14 is published as a range across the criterion, asserting neither side.
  · Watch-item ages step by exactly ONE from LATEST_STATE.md.
  · Run the superlative sweep before you finish: first / most / highest / strongest / nth time /
    since ed. N each needs a source or a stated basis, or it gets cut.
  · Do not publish a figure you did not retrieve this run.

Write the DBS one-pager and the FULL brief into templates/, then run `daybreak build`.
"""


def cmd_draft(a):
    p = paths(a.date)
    if not p["facts"].exists():
        print(f"{C['r']}no facts for {a.date} — run `daybreak fetch` first{C['x']}")
        return 2
    prompt = PROMPT.format(ed=edition_for(a.date), date=a.date)
    (OUT / f"prompt_{a.date}.txt").write_text(prompt)
    if a.print_prompt:
        print(prompt)
        return 0
    claude = a.claude_bin or "claude"
    print(f"{C['b']}daybreak draft{C['x']}  handing off to `{claude} -p` …")
    try:
        r = subprocess.run([claude, "-p", prompt], cwd=str(HERE.parent), timeout=a.timeout)
        return r.returncode
    except FileNotFoundError:
        print(f"{C['y']}`{claude}` not found.{C['x']}  The prompt is at "
              f"out/prompt_{a.date}.txt — paste it into Claude by hand, or run "
              f"`daybreak build --degraded` for a facts-only edition.")
        return 3
    except subprocess.TimeoutExpired:
        print(f"{C['r']}draft timed out after {a.timeout}s.{C['x']}  "
              f"Fall back to `daybreak build --degraded`.")
        return 3


def cmd_build(a):
    """Delegates to the render scripts that already exist in ../scripts/."""
    p = paths(a.date)
    if a.degraded:
        if not p["facts"].exists():
            print(f"{C['r']}degraded build needs facts — run fetch first{C['x']}")
            return 2
        md = degraded_markdown(json.loads(p["facts"].read_text()),
                               json.loads(p["gates"].read_text()) if p["gates"].exists() else {})
        p["brief"].write_text(md)
        print(f"{C['y']}DEGRADED BUILD{C['x']} — facts only, no prose → {p['brief']}")
        return 0
    scripts = HERE.parent / "scripts"
    steps = [("chart+map raster", ["node", str(scripts / "mkmap.js")]),
             ("PDF render",       ["node", str(scripts / "render.js")]),
             ("DOCX autotune",    [sys.executable, str(scripts / "autotune.py")])]
    for name, cmd in steps:
        if not Path(cmd[1]).exists():
            print(f"  {C['y']}skip{C['x']} {name} (missing {Path(cmd[1]).name})")
            continue
        print(f"  {C['b']}run {C['x']}{name}")
        subprocess.run(cmd, cwd=str(HERE.parent))
    return 0


def degraded_markdown(facts, g):
    """The 4 AM fallback. No judgement, no prose — just what was retrieved."""
    L = [f"# DAYBREAK BRIEF — ATX-DB-2026-{facts['edition']} — {facts['date']}",
         "", "> **DEGRADED EDITION.** Machine-collected facts only. No analysis, no chips, "
         "no watch-item narrative. Everything below was retrieved automatically at "
         f"{facts['generated_at']}. Treat every line as raw source material.", ""]
    fc = next((r for r in facts["results"] if r["id"] == "nws_point_forecast" and r["ok"]), None)
    if fc:
        L += ["## Weather", "", "| Period | Temp | Heat index | POP | Forecast |",
              "|---|---|---|---|---|"]
        for p in fc["data"]["periods"][:6]:
            L.append(f"| {p['name']} | {p['temperature']}° | "
                     f"{p['heat_index'] or '—'} | {p['pop'] if p['pop'] is not None else '—'}% | "
                     f"{p['shortForecast']} |")
        L += ["", f"*Product issued {fc['data'].get('updateTime')}*", ""]
    al = next((r for r in facts["results"] if r["id"] == "nws_alerts" and r["ok"]), None)
    if al:
        n = al["data"]["count"]
        L += ["## Active alerts", "",
              "**None in force.**" if n == 0 else
              "\n".join(f"- **{x['event']}** — {x['headline']}" for x in al["data"]["alerts"]), ""]
    cli = next((r for r in facts["results"] if r["id"] == "nws_cli_att" and r["ok"]), None)
    if cli:
        L += ["## Observed (Camp Mabry climate report)", "", "| Summary for | Max | Min | Precip |",
              "|---|---|---|---|"]
        for pr in cli["data"]["products"]:
            if pr.get("max"):
                L.append(f"| {pr.get('summary_for')} | {pr['max']}° "
                         f"{pr.get('max_time') or ''} | {pr.get('min')}° | {pr.get('precip')} |")
        L.append("")
    dead = [r for r in facts["results"] if not r["ok"]]
    if dead:
        L += ["## ⚠ NOT VERIFIED THIS PASS", "",
              "These sources did not answer. Nothing below them was estimated.", ""]
        L += [f"- **{r['row']['name']}** — {r['error']}" for r in dead] + [""]
    if g.get("G14", {}).get("findings"):
        L += ["## ⚠ THRESHOLD WATCH (G14)", ""]
        for f in g["G14"]["findings"]:
            L.append(f"- **{f['period']}** {f['field']} {f['prior']} → {f['current']} "
                     f"against {f['criterion']} ({f['threshold']}). {f['verdict']}")
        L.append("")
    L += ["---", "*Internal — Not For Guest Distribution. Generated in degraded mode; "
          "a full edition supersedes this one.*"]
    return "\n".join(L)


def cmd_publish(a):
    script = HERE.parent / "scripts" / "mkweb.py"
    if not script.exists():
        print(f"{C['r']}scripts/mkweb.py not found{C['x']}")
        return 2
    return subprocess.run([sys.executable, str(script)], cwd=str(HERE.parent)).returncode


def cmd_status(a):
    src = load_sources()
    print(f"{C['b']}daybreak{C['x']}  manifest v{src['version']}  "
          f"{len(src['tier1'])} Tier-1 rows  {len(src['tier2'])} Tier-2 triggers")
    print(f"  today = {_date.today()}  →  ed. {edition_for(str(_date.today()))}")
    for f in sorted(OUT.glob("facts_*.json"))[-5:]:
        d = json.loads(f.read_text())
        dead = sum(1 for r in d["results"] if not r["ok"])
        col = C["g"] if dead == 0 else C["y"]
        print(f"  {d['date']}  ed. {d['edition']}  "
              f"{col}{len(d['results']) - dead}/{len(d['results'])} sources{C['x']}")
    return 0


def main():
    ap = argparse.ArgumentParser(prog="daybreak", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    today = str(_date.today())

    f = sub.add_parser("fetch", help="walk the manifest, run the gates")
    f.add_argument("--date", default=today)
    f.add_argument("--rows", help="comma-separated row numbers, e.g. 1,4,20")
    f.add_argument("--double-read", action="store_true", default=True,
                   help="G14: read the forecast twice (default on)")
    f.add_argument("--no-double-read", dest="double_read", action="store_false")
    f.add_argument("--reread-delay", type=int, default=90)
    f.set_defaults(fn=cmd_fetch)

    g = sub.add_parser("gates", help="re-print the gate report")
    g.add_argument("--date", default=today); g.set_defaults(fn=cmd_gates)

    d = sub.add_parser("draft", help="hand the facts to a model")
    d.add_argument("--date", default=today)
    d.add_argument("--print-prompt", action="store_true")
    d.add_argument("--claude-bin"); d.add_argument("--timeout", type=int, default=1800)
    d.set_defaults(fn=cmd_draft)

    b = sub.add_parser("build", help="render the six files")
    b.add_argument("--date", default=today)
    b.add_argument("--degraded", action="store_true", help="facts-only, no model needed")
    b.set_defaults(fn=cmd_build)

    p = sub.add_parser("publish", help="push the web version"); p.add_argument("--date", default=today)
    p.set_defaults(fn=cmd_publish)

    s = sub.add_parser("status", help="what has run lately"); s.set_defaults(fn=cmd_status)

    a = ap.parse_args()
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()
