# DAYBREAK BRIEF — PORTABLE KNOWLEDGE BASE
### Everything needed to produce the brief from any machine. Start on this page.

**The product:** a daily internal awareness brief for Four Seasons Hotel Austin.
A **DBS** one-pager and a **FULL** multi-page, each in HTML + PDF + DOCX — six files a day.
Issued **0600 CDT**. Serial **ATX-DB-2026-NNN**. **Ed. 250 = 6 September 2026**; the number
is arithmetic on the date, never a guess.

---

## Pick your situation

| Your situation | Go to | Time |
|---|---|---|
| **Normal morning, machine works** | `1_RUN/cli/` → `python3 daybreak.py fetch` | ~25 min |
| **No Claude, but Copilot works** | `1_RUN/COPILOT_FALLBACK.md` | ~30 min |
| **Doing it entirely by hand** | `1_RUN/RUNBOOK.md` | ~90 min |
| **New machine, nothing set up** | `2_METHOD/MIGRATION.md` | ~10 min |
| **Handing this to another AI** | `3_STATE/` then `2_METHOD/` — order below | — |
| **Something looks wrong in a past edition** | `2_METHOD/VERIFICATION_RULES.md` | — |
| **IT / distribution / permissions** | `6_ADMIN/` | — |

---

## The one idea everything here is built on

> ## Automate a **LIST**, never a **JUDGEMENT**.

On **ed. 249** the brief shipped without mentioning that Texas played its home opener at DKR
that afternoon — a ~100,000-seat stadium 1.5 miles north, campus streets closed, towing
enforced. Every venue that had mattered on previous days *was* checked. Nothing forced a
check of UT football, because "check the venues" was a judgement call.

Everything in this folder follows from that:

```
   a LIST of 23 sources        →  2_METHOD/SOURCE_MANIFEST.md
   a GATE that walks the list  →  1_RUN/cli/gates.py   (G13)
   a GATE for numbers near a
     decision threshold        →  1_RUN/cli/gates.py   (G14)
   RULES written from real
     published mistakes        →  2_METHOD/VERIFICATION_RULES.md
```

**A source that cannot be reached is published as "not verified this pass."**
**Nothing is estimated. Silence is the only forbidden outcome.**

---

## What is in each folder

```
1_RUN/        Do today's edition.
              cli/          the pipeline — fetch · draft · build · publish
              RUNBOOK.md    the manual steps, if the pipeline is unavailable
              COPILOT_FALLBACK.md   producing it on a locked network with M365 Copilot

2_METHOD/     Why it is the way it is. Read before changing anything.
              SOURCE_MANIFEST.md    the 23 rows, and WHY each one exists
              VERIFICATION_RULES.md 12 rules — every one from a real published error
              HOUSE_STYLE.md        voice, chip levels, flag bands, section order
              PIPELINE.md           how the six files actually get rendered
              MIGRATION.md          cold-start on a machine that has nothing

3_STATE/      What the next edition inherits. READ FIRST, EVERY TIME.
              LATEST_STATE.md   watch-item ages, chips, corrections not to repeat
              memory/           the full project record, ed. 246 → 251, plus the
                                workflow and automation notes

4_BUILD/      The assets that turn text into the six files.
              templates/  scripts/  config/artifact.json  ← the stable team URL

5_EDITIONS/   The archive. The last few real editions are the best spec there is.
              2026-09-01 … 2026-09-07/   _web_versions/

6_ADMIN/      Distribution, permissions, the team.
              AUTOMATION_OPTIONS.html   the visual guide to deployment choices
              IT_REQUEST_sharepoint.md · IT_REQUEST_network.md · TEAM_GUIDE.md
```

---

## Ten-minute cold start on a new machine

```bash
cd 1_RUN/cli
python3 daybreak.py status            # manifest version + today's edition number
python3 daybreak.py fetch             # ~2 min including the G14 re-read pause
python3 daybreak.py build --degraded  # a real, publishable, facts-only brief
```

**No `pip install`. Standard library only.** Node + Playwright are needed only for the
403 fallback and the PDF/DOCX render — without them you still get `fetch`, `gates` and
`build --degraded`, which is the point of the split.

If that works, you have a working pipeline. Everything after it is quality, not capability.

---

## Handing this to a fresh AI instance

Give it these, in this order. **The first one matters more than the rest combined.**

1. `3_STATE/LATEST_STATE.md` — what carried forward, what corrections not to reintroduce,
   what the watch-item ages are.
2. `2_METHOD/VERIFICATION_RULES.md` — the 12 rules.
3. `2_METHOD/HOUSE_STYLE.md` — the voice.
4. `3_STATE/memory/daybreak_brief.md` — the full production workflow, including every
   source that works, every source that does not, and the traps in each.
5. The most recent folder in `5_EDITIONS/` — a worked example beats a description.

`python3 1_RUN/cli/daybreak.py draft --print-prompt` prints the handoff prompt with the
hard constraints already in it. **Start there rather than writing your own.**

**The three things a new instance gets wrong:**
- Publishing a figure it did not retrieve this session *(rule 1)*
- Treating an unreachable source as a source that said nothing *(rule 11 / G13)*
- Asserting a forecast number that sits near a criterion off a single read *(rule 12 / G14)*

---

## Two facts that will save you an hour

**Use `api.weather.gov`, not the rendered NWS pages.** Ed. 250 lost four Tier-1 sources to
`forecast.weather.gov` — the climate report served the wrong product on every version index
and both observation histories redirect-looped. **All four answered first try on the service
endpoints.** When a source fails repeatedly, question the *route* before the source.

**Republish the web version to the STORED URL** in `4_BUILD/config/artifact.json`.
Publishing without it creates a new artifact every day and the team's bookmark goes stale.

---

*Assembled 7 September 2026, after ed. 251. This folder is portable and self-contained —
copy the whole `DAYBREAK_BRIEF` directory to any machine and start at this page again.*
