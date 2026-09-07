"""
Daybreak Brief — the gates.

G13  SOURCE COVERAGE   — every Tier-1 row is fetched, or the run is marked FAILED.
                         A source that cannot be reached is published as
                         "not verified this pass". Silence is the only forbidden outcome.
                         (Written after ed. 249 shipped without the UT home opener.)

G14  THRESHOLD RE-READ — any forecast figure sitting within `threshold_margin` of a
                         named criterion gets a second read. If two reads straddle the
                         criterion, publish BOTH and assert NEITHER side of the line.
                         (Written after ed. 250 asserted a 109 heat index — and therefore
                         "above the 108 advisory criterion" — when the issuance an hour
                         earlier had said 107.)

Neither gate is a judgement. Both are loops.
"""

OPS = {">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b,
       ">": lambda a, b: a > b,   "<": lambda a, b: a < b}


def g13(results, tier1, partial=False):
    """Returns (status, report). status is PASS | DEGRADED | PARTIAL | FAIL.

    `partial=True` means the operator deliberately ran a subset (--rows). Rows that
    were never attempted are then expected, not a defect: the run is PARTIAL and
    must not be published as an edition. A gate that cries wolf on a deliberate
    subset teaches the operator to ignore it, which is worse than having no gate.
    """
    by_id = {r["id"]: r for r in results}
    rows = []
    missing, failed = [], []
    for row in tier1:
        r = by_id.get(row["id"])
        if r is None:
            rows.append({"n": row["n"], "id": row["id"], "state": "NOT ATTEMPTED"})
            missing.append(row)
            continue
        rows.append({"n": row["n"], "id": row["id"],
                     "state": "ok" if r["ok"] else "UNREACHABLE",
                     "error": r.get("error")})
        if not r["ok"]:
            failed.append(row)

    if missing and partial:
        status = "PARTIAL"       # deliberate subset - NOT publishable, but not a defect
    elif missing:
        status = "FAIL"          # a full run that skipped a row is a broken build
    elif failed:
        status = "DEGRADED"      # tried and dead -> publish as a gap, keep going
    else:
        status = "PASS"

    return status, {
        "gate": "G13 SOURCE COVERAGE",
        "status": status,
        "attempted": len(results),
        "tier1_total": len(tier1),
        "unreachable": [{"n": f["n"], "id": f["id"], "name": f["name"],
                         "rule": f.get("rule", ""),
                         "error": by_id[f["id"]].get("error")} for f in failed],
        "not_attempted": [{"n": m["n"], "id": m["id"], "name": m["name"]} for m in missing],
        "publish_instruction": (
            "PARTIAL: a subset was run on purpose. DO NOT PUBLISH an edition from this "
            "run - re-run without --rows first."
            if status == "PARTIAL" else
            "Every UNREACHABLE row must appear in the confidence note as "
            "'not verified this pass'. Do not estimate. Do not omit."),
    }


def _near(value, th, margin):
    return value is not None and abs(value - th["value"]) <= margin


def g14(current_periods, prior_periods, thresholds, margin):
    """
    current_periods / prior_periods: lists of parsed forecast periods, from two
    reads of the same product (this run's double-read, or this run vs the last).
    Compares any figure near a criterion and flags a straddle.
    """
    prior_by_name = {p.get("name"): p for p in (prior_periods or [])}
    findings, straddles = [], 0

    for p in current_periods:
        prior = prior_by_name.get(p.get("name"))
        for th in thresholds:
            cur = p.get(th["field"])
            if not _near(cur, th, margin):
                continue
            pv = prior.get(th["field"]) if prior else None
            op = OPS[th["op"]]
            cur_side = op(cur, th["value"])
            prior_side = op(pv, th["value"]) if pv is not None else None

            f = {"period": p.get("name"), "field": th["field"], "criterion": th["name"],
                 "threshold": th["value"], "current": cur, "prior": pv,
                 "current_meets": cur_side, "prior_meets": prior_side, "straddle": False}

            if pv is None:
                f["verdict"] = ("NEAR A CRITERION and there is no second read to compare. "
                                "FETCH THE PRECEDING ISSUANCE BEFORE ASSERTING A SIDE.")
            elif prior_side != cur_side:
                f["straddle"] = True
                straddles += 1
                lo, hi = sorted([pv, cur])
                f["verdict"] = (f"STRADDLE. Two issuances disagree across the {th['name']} "
                                f"criterion ({th['op']} {th['value']}). PUBLISH BOTH: "
                                f"\"unsettled {lo}-{hi}, straddling the line\". "
                                f"Assert neither side. Plan for the worse, re-check first thing.")
            elif pv != cur:
                f["verdict"] = (f"Moved {pv} -> {cur} but both reads land on the same side "
                                f"of the criterion. Safe to assert; name the movement.")
            else:
                f["verdict"] = "Two reads agree. Safe to assert."
            findings.append(f)

    return ("STRADDLE" if straddles else "PASS" if findings else "N/A"), {
        "gate": "G14 THRESHOLD RE-READ",
        "status": "STRADDLE" if straddles else ("PASS" if findings else "N/A — no figure near a criterion"),
        "margin": margin,
        "findings": findings,
        "publish_instruction": (
            "A range that spans a decision point is more honest AND more useful than a "
            "single number on one side of it."),
    }
