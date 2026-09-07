"""
Daybreak Brief — collectors.
Standard library ONLY. No pip install, on purpose: this has to run on a machine
nobody has set up, five years from now, possibly by someone who is not Ryan.

Every collector returns the same shape:

    {"ok": bool, "id": str, "fetched_at": iso8601, "url": str,
     "data": {...}          # parsed, when the source has structure
     "raw": str,            # what came back, saved to raw/ for the draft stage
     "error": str|None}

A collector NEVER raises. A dead source is a published gap, not a crash.
"""

import json, re, ssl, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

TIMEOUT = 30
RETRIES = 3
BACKOFF = 2.0
API = "https://api.weather.gov"


def _now():
    return datetime.now(timezone.utc).isoformat()


BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")


def _get(url, ua, accept=None, tries=RETRIES):
    """One HTTP GET with retries. Returns (body_text, error_or_None).
    A 403 is retried once with a browser User-Agent: several sources (texassports,
    the Hormuz tracker) refuse the stdlib agent but serve the same public page."""
    last = None
    agents = [ua, BROWSER_UA]
    for attempt in range(tries):
        ua = agents[min(attempt, 1)]
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": ua,
                "Accept": accept or "text/html,application/xhtml+xml,*/*",
            })
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
                return r.read().decode("utf-8", errors="replace"), None
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code == 404 or e.code == 410:
                break                      # not transient; stop burning time
            if e.code == 403 and attempt >= 1:
                break                      # already retried with the browser agent
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
        if attempt < tries - 1:
            time.sleep(BACKOFF * (attempt + 1))
    return None, last


def _res(sid, url, ok, raw=None, data=None, error=None):
    return {"id": sid, "url": url, "ok": ok, "fetched_at": _now(),
            "raw": raw, "data": data or {}, "error": error}


# ---------------------------------------------------------------- NWS API ---

HEAT_RE = re.compile(r"[Hh]eat index (?:values )?(?:as high as|near|around|up to)?\s*(\d{2,3})")
HIGH_RE = re.compile(r"[Hh]igh near (\d{2,3})")
LOW_RE  = re.compile(r"[Ll]ow around (\d{2,3})")
POP_RE  = re.compile(r"[Cc]hance of precipitation is (\d{1,3})%")


def parse_period(p):
    """Pull the numbers we assert out of a worded forecast period."""
    txt = p.get("detailedForecast", "") or ""
    out = {
        "name": p.get("name"),
        "isDaytime": p.get("isDaytime"),
        "temperature": p.get("temperature"),
        "startTime": p.get("startTime"),
        "shortForecast": p.get("shortForecast"),
        "detailedForecast": txt,
        "heat_index": None, "high": None, "low": None, "pop": None,
    }
    for key, rx in (("heat_index", HEAT_RE), ("high", HIGH_RE), ("low", LOW_RE), ("pop", POP_RE)):
        m = rx.search(txt)
        if m:
            out[key] = int(m.group(1))
    # NWS also exposes POP structurally on newer responses
    if out["pop"] is None and isinstance(p.get("probabilityOfPrecipitation"), dict):
        out["pop"] = p["probabilityOfPrecipitation"].get("value")
    return out


def nws_forecast(sid, cfg, ua):
    gx, gy = cfg["grid"]
    url = f"{API}/gridpoints/{cfg['office']}/{gx},{gy}/forecast"
    body, err = _get(url, ua, accept="application/geo+json")
    if err:
        return _res(sid, url, False, error=err)
    try:
        props = json.loads(body)["properties"]
        periods = [parse_period(p) for p in props.get("periods", [])[:8]]
        return _res(sid, url, True, raw=body, data={
            "updateTime": props.get("updateTime"),
            "generatedAt": props.get("generatedAt"),
            "periods": periods,
        })
    except Exception as e:
        return _res(sid, url, False, raw=body, error=f"parse: {e}")


def nws_alerts(sid, cfg, ua):
    url = f"{API}/alerts/active?point={cfg['lat']},{cfg['lon']}"
    body, err = _get(url, ua, accept="application/geo+json")
    if err:
        return _res(sid, url, False, error=err)
    try:
        feats = json.loads(body).get("features", [])
        alerts = [{"event": f["properties"].get("event"),
                   "headline": f["properties"].get("headline"),
                   "severity": f["properties"].get("severity"),
                   "onset": f["properties"].get("onset"),
                   "ends": f["properties"].get("ends")} for f in feats]
        return _res(sid, url, True, raw=body,
                    data={"count": len(alerts), "alerts": alerts})
    except Exception as e:
        return _res(sid, url, False, raw=body, error=f"parse: {e}")


CLI_MAX = re.compile(r"^\s*MAXIMUM\s+(-?\d+)\s+(\d{1,2}:\d{2}\s*[AP]M)?", re.M)
CLI_MIN = re.compile(r"^\s*MINIMUM\s+(-?\d+)\s+(\d{1,2}:\d{2}\s*[AP]M)?", re.M)
CLI_FOR = re.compile(r"CLIMATE SUMMARY FOR\s+(.+?)\.{0,3}\s*$", re.M)
CLI_PCP = re.compile(r"^\s*YESTERDAY\s+([\d.T]+)", re.M)


def nws_product(sid, cfg, ua, ptype="CLI", loc="ATT", count=4):
    """Fetch the last `count` issuances of a text product. This is the endpoint
    that replaced product.php, which served the wrong product on ed. 250."""
    idx = f"{API}/products/types/{ptype}/locations/{loc}"
    body, err = _get(idx, ua, accept="application/ld+json")
    if err:
        return _res(sid, idx, False, error=err)
    try:
        graph = json.loads(body).get("@graph", [])[:count]
    except Exception as e:
        return _res(sid, idx, False, raw=body, error=f"parse index: {e}")
    if not graph:
        return _res(sid, idx, False, error="index returned no products")

    products = []
    for p in graph:
        txt, e2 = _get(f"{API}/products/{p['id']}", ua, accept="application/ld+json")
        if e2:
            products.append({"id": p["id"], "issued": p.get("issuanceTime"), "error": e2})
            continue
        try:
            text = json.loads(txt).get("productText", "")
        except Exception:
            text = txt
        item = {"id": p["id"], "issued": p.get("issuanceTime"), "text": text}
        if ptype == "CLI":
            mx, mn = CLI_MAX.search(text), CLI_MIN.search(text)
            forr, pcp = CLI_FOR.search(text), CLI_PCP.search(text)
            item["summary_for"] = forr.group(1).strip() if forr else None
            item["max"] = int(mx.group(1)) if mx else None
            item["max_time"] = mx.group(2) if mx and mx.group(2) else None
            item["min"] = int(mn.group(1)) if mn else None
            item["precip"] = pcp.group(1) if pcp else None
        products.append(item)
    return _res(sid, idx, True, data={"type": ptype, "location": loc, "products": products})


def nws_obs(sid, cfg, ua, station="KATT", hours=30):
    start = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:00:00Z")
    url = f"{API}/stations/{station}/observations?start={start}"
    body, err = _get(url, ua, accept="application/geo+json")
    if err:
        return _res(sid, url, False, error=err)
    try:
        feats = json.loads(body).get("features", [])
        obs = []
        for f in feats:
            pr = f["properties"]
            def c2f(v):
                return None if v is None else round(v * 9 / 5 + 32, 1)
            obs.append({"t": pr.get("timestamp"),
                        "temp_f": c2f((pr.get("temperature") or {}).get("value")),
                        "heat_index_f": c2f((pr.get("heatIndex") or {}).get("value")),
                        "dewpoint_f": c2f((pr.get("dewpoint") or {}).get("value"))})
        temps = [o["temp_f"] for o in obs if o["temp_f"] is not None]
        hidx = [o["heat_index_f"] for o in obs if o["heat_index_f"] is not None]
        return _res(sid, url, True, data={
            "station": station, "count": len(obs),
            "latest": obs[0] if obs else None,
            "window_max_temp_f": max(temps) if temps else None,
            "window_max_heat_index_f": max(hidx) if hidx else None,
            "_window_note": f"rolling {hours}h window — NOT a calendar-day maximum (ed. 250 trap)",
            "observations": obs[:40]})
    except Exception as e:
        return _res(sid, url, False, raw=body, error=f"parse: {e}")


# ------------------------------------------------------------------ generic --

TAG = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)
STRIP = re.compile(r"<[^>]+>")


def http(sid, cfg, ua, url=None):
    body, err = _get(url, ua)
    if err:
        return _res(sid, url, False, error=err)
    text = STRIP.sub(" ", TAG.sub(" ", body))
    text = re.sub(r"&nbsp;?", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return _res(sid, url, True, raw=body,
                data={"bytes": len(body), "text_excerpt": text[:6000]})


KIND = {"nws_forecast": nws_forecast, "nws_alerts": nws_alerts,
        "nws_product": nws_product, "nws_obs": nws_obs, "http": http}


def run_row(row, cfg, ua):
    fn = KIND.get(row["kind"])
    if not fn:
        return _res(row["id"], "", False, error=f"unknown kind {row['kind']}")
    try:
        return fn(row["id"], cfg, ua, **row.get("args", {}))
    except Exception as e:                     # a collector must never crash the run
        return _res(row["id"], "", False, error=f"collector crashed: {type(e).__name__}: {e}")
