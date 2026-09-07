# MIGRATION — standing the Daybreak Brief up somewhere else

**Read this if you are on a new machine, a new account, or you are an AI instance
being handed this project cold.** It assumes nothing.

The product: a daily internal awareness brief for Four Seasons Hotel Austin.
Two documents — a **DBS** one-pager and a **FULL** multi-page — each in HTML, PDF
and DOCX. Six files a day. Issued 0600 CDT. Serial `ATX-DB-2026-<edition>`.
**Ed. 250 = 6 September 2026.** The edition number is arithmetic on the date, not a guess.

---

## 0. The one thing to understand first

> **Automate a LIST, never a JUDGEMENT.**

Ed. 249 shipped without mentioning that Texas played its home opener at DKR that
afternoon — ~100,000 seats, 1.5 miles north, campus streets closed, towing enforced.
Every venue that had mattered on previous days *was* checked. Nothing forced a check
of UT football, because "check the venues" was a judgement call.

Everything in this project follows from that: the manifest, both gates, the degraded
mode, the source-recheck pass. **A source is either on the list and fetched, or the
build fails. A source that cannot be reached is published as a gap. Silence is the
only forbidden outcome.**

---

## 1. What to copy

Copy the whole `DAYBREAK_KB/` folder. It is self-contained and portable by design.

```
DAYBREAK_KB/
  00_START_HERE.md          read this second
  01_SOURCE_MANIFEST.md     the 23 rows in prose, with WHY each exists
  02_RUNBOOK.md             the 14 steps of producing one edition by hand
  03_HOUSE_STYLE.md         voice, chip levels, flag bands, section order
  04_PIPELINE.md            how the six files are actually rendered
  05_VERIFICATION_RULES.md  12 rules, EVERY ONE written from a real published error
  06_COPILOT_FALLBACK.md    producing the brief with M365 Copilot on a locked network
  MIGRATION.md              ← you are here
  AUTOMATION_OPTIONS.html   the visual guide to the deployment choices
  IT_REQUEST.md             what to ask hotel IT for (hosting/distribution)
  IT_REQUEST_NETWORK.md     what to ask hotel IT for (network reachability)
  cli/                      the pipeline — see cli/README.md
  scripts/                  render.js · measure.sh · mkdocx.{py,js} · mkmap.js · autotune.py · mkweb.py
  templates/                TEMPLATE_DBS.html · TEMPLATE_FULL.html
  state/LATEST_STATE.md     WHAT THE LAST EDITION CARRIED FORWARD — read before drafting
  team/TEAM_GUIDE.md        the simple instructions + FAQ for staff
  config/artifact.json      the published web artifact's URL — DO NOT lose this
```

---

## 2. Prerequisites on the new machine

| Need | For | Check |
|---|---|---|
| **Python 3.9+** | the whole CLI | `python3 --version` |
| Node 18+ | PDF/DOCX render, 403 fallback | `node --version` |
| Playwright + Chromium | same | `npx playwright install chromium` |
| A Claude license *or* API key | the `draft` stage only | `claude --version` |

**Nothing else. No `pip install`.** If Node is missing you still get `fetch`,
`gates` and `build --degraded` — which is the whole point of the split.

---

## 3. Ten-minute cold start

```bash
cd DAYBREAK_KB/cli
python3 daybreak.py status                   # sanity: manifest version, today's edition number
python3 daybreak.py fetch                    # ~2 min including the G14 re-read pause
python3 daybreak.py build --degraded         # a real, publishable, facts-only brief
open out/brief_$(date +%F).md
```

If that works you have a working pipeline. Everything after this is quality, not capability.

Then, for a full edition:

```bash
python3 daybreak.py draft --print-prompt     # paste into Claude if `claude` isn't installed
python3 daybreak.py build
python3 daybreak.py publish
```

---

## 4. Handing this to a fresh AI instance

Give it, in this order:

1. `state/LATEST_STATE.md` — **the single most important file.** What carried forward,
   what corrections not to reintroduce, what the watch-item ages are.
2. `05_VERIFICATION_RULES.md` — the 12 rules.
3. `03_HOUSE_STYLE.md` — the voice.
4. `out/facts_<date>.json` + `out/gates_<date>.json` — this run's material.
5. `02_RUNBOOK.md` — if it is producing the edition by hand.

`python3 daybreak.py draft --print-prompt` prints the exact handoff prompt with the
hard constraints already in it. Start there rather than writing your own.

**The three things a new instance gets wrong:**
- Publishing a figure it did not retrieve this session (rule 1).
- Treating an unreachable source as a source that said nothing (rule 11 / G13).
- Asserting a forecast number that sits near a criterion off one read (rule 12 / G14).

---

## 5. Scheduling

### On a Mac (the default; uses the existing subscription, costs nothing)
```bash
cp deploy/com.rowanrisk.daybreak.plist ~/Library/LaunchAgents/
# edit the three paths inside it first
launchctl load ~/Library/LaunchAgents/com.rowanrisk.daybreak.plist
launchctl start com.rowanrisk.daybreak          # test now; do not wait for 3:30 AM
sudo pmset repeat wakeorpoweron MTWRFSU 03:25:00   # THE MACHINE MUST BE AWAKE
pmset -g sched                                   # confirm
```
**Failure mode: the laptop is closed.** That is the entire risk of this option, and
it is why `pmset` is not optional.

### In the cloud (runs whether or not any machine is on; costs metered tokens)
`deploy/github-actions-daybreak.yml` → `.github/workflows/daybreak.yml`.
Needs `ANTHROPIC_API_KEY` as a repo secret. Note the two cron lines: GitHub cron is
UTC and does not follow daylight saving.

**A subscription is licensed for your own use.** Running the pipeline on your own
machine on a timer is ordinary. Standing up a service that generates for the whole
property is the point at which a metered API key is the correct instrument — and
that is a billable business expense, not a problem.

---

## 6. Distribution

| Route | Status |
|---|---|
| Web artifact on claude.ai | Published daily to the URL in `config/artifact.json`. **Republish to that stored URL — a new publish makes a NEW artifact and the bookmark dies.** |
| Google Drive | **Does not work on the hotel network.** |
| SharePoint folder + non-expiring org link | The ask in `IT_REQUEST.md`. Smallest ask, and the legally safest. |
| Teams post | Power Automate **Workflows**. O365 connectors and Incoming Webhooks were **fully retired 22 May 2026** — anyone offering a webhook URL is working from stale documentation. |
| Email auto-forward | External auto-forwarding is off by default (NDR `5.7.520`) and a standard user cannot override it. |

**Two tests decide everything, and neither has been run yet:**
1. Does `claude.ai` even resolve from a hotel machine?
2. Does the shared artifact URL open in a private window with no sign-in?

---

## 7. Legal shape — do not lose this by accident

Distribution runs through the **employee–employer exemption, Texas Occupations Code
§1702.323**: the hotel owns the destination and staff put the file there. The Tier-3
enterprise pattern (an Entra app registration with Graph `Sites.Selected` pushing into
the tenant) is the **vendor-integration** fact pattern — precisely what §1702.323
depends on *not* establishing. `IT_REQUEST.md` explains this.

**The smallest ask is also the safest one.** That alignment is convenient; don't spend it.

---

## 8. If you change one thing, change the manifest

`cli/sources.json` is the control. When a miss is found, add the row **that day**.
The `rule` field is printed back at whoever is standing there when the row dies, so
write it as an instruction to a tired person at 4 AM — not as a description.

Then mirror it in `01_SOURCE_MANIFEST.md`, which is the human-readable copy, and add
the error to `05_VERIFICATION_RULES.md`. Every rule in that file cost a published mistake.
