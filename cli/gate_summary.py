#!/usr/bin/env python3
"""
Render a gate report as GitHub-flavoured markdown for the Actions run summary.

    python3 gate_summary.py out/gates_2026-09-09.json >> "$GITHUB_STEP_SUMMARY"

Lives in the repo rather than inline in the workflow on purpose: an inline
heredoc inside a YAML block scalar has to stay indented, and when it does not
the whole workflow fails to parse with no job and no log. That is exactly how
the first run of this workflow failed. Keep generators in files.
"""
import json
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: gate_summary.py <gates_YYYY-MM-DD.json>", file=sys.stderr)
        return 2
    try:
        g = json.load(open(sys.argv[1]))
    except FileNotFoundError:
        print("No gate report was produced - the fetch stage did not get that far.")
        return 0
    except json.JSONDecodeError as e:
        print(f"Gate report is not readable JSON: {e}")
        return 0

    a = g.get("G13", {})
    b = g.get("G14", {})
    reachable = a.get("attempted", 0) - len(a.get("unreachable", []))

    out = [
        f"## Gates - {a.get('status', 'UNKNOWN')}",
        "",
        f"**G13 SOURCE COVERAGE - {a.get('status', '?')}**  ",
        f"{reachable} of {a.get('attempted', 0)} sources reachable",
        "",
    ]

    for u in a.get("unreachable", []):
        out.append(f"- WARN **row {u.get('n')} {u.get('name')}** - `{u.get('error')}` "
                   f"- must be published as a gap")
    na = a.get("not_attempted", [])
    if na:
        nums = ", ".join(str(x.get("n")) for x in na)
        out.append(f"- STOP **{len(na)} rows never attempted**: {nums}")
    if not a.get("unreachable") and not na:
        out.append("- OK every manifest row answered")

    out += ["", f"**G14 THRESHOLD RE-READ - {b.get('status', 'N/A')}**", ""]
    findings = b.get("findings", [])
    if not findings:
        out.append("- no forecast figure sits near a named criterion")
    for f in findings:
        icon = "WARN" if f.get("straddle") else "-"
        out.append(f"- {icon} **{f.get('period')}** {f.get('field')} "
                   f"{f.get('prior')} -> {f.get('current')} vs {f.get('criterion')} "
                   f"{f.get('threshold')}")
        out.append(f"  - {f.get('verdict')}")

    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
