---
name: automation
description: The scheduled-task architecture for the daily brief — the cloud-native repo, the 12 gates, the DOCX pipeline and its hard-won rules, Ryan's standing decisions on email and autonomy, and the SharePoint/Teams distribution findings. Read before changing how editions are produced or delivered.
type: project
---
**Decided 3 Sep 2026.** Ryan asked to automate the daily brief for a 05:00 CT deadline, with a phone alert he can act on away from his Mac.

## ⚠️ THE ARCHITECTURAL CONSTRAINT THAT DRIVES EVERYTHING
`project_memory_*`, `device_bash` and the `4SDAB_Design` folder **all run through the link to Ryan's MacBook, which is asleep at 03:15**. A scheduled run cannot use any of them. **The system of record is therefore a private GitHub repo**, not project memory: runbook, templates, carry-forward state and the edition archive all live there. `git clone`/`push` to github.com is **verified working** from the cloud container. Committing to the iCloud folder is best-effort, for whenever the Mac is up. (The link dropped mid-session on 3, 4 and 5 Sep and came back each time — `SendUserFile` kept working throughout; **keep the file_uuids and commit when it returns**. On 4 Sep the commit had to wait until the next day and the uuids were still valid.)
**⚠️ Say "the link to your Mac" to Ryan, never "the bridge."** He asked what that meant on 5 Sep, and it collides badly with a brief that talks about the Congress Avenue bridge.

## Verified egress from the cloud container (probed 3 Sep with real payloads, not just status codes)
- ✅ **github.com / api.github.com** — `git ls-remote` succeeds
- ✅ **graph.microsoft.com + login.microsoftonline.com** — real 401, so SharePoint is technically reachable
- ✅ **HTTPS email APIs** — Resend, Postmark, SendGrid, Gmail API all reachable
- ❌ **SMTP** — ports 465/587 **blocked**. SMTP is not an option, ever.
- Google Drive connector connected and live; Gmail connector installed org-level but toggled off in chat; the M365 connector is **read-only** and cannot write a file.

## Ryan's standing decisions
1. **Autonomy: publish unless a gate fails.** A failure holds the edition on `draft/YYYYMMDD`, leaves `main` untouched, and alerts.
2. **Email: OFF, but wired and one flag away** (`config/email.json` → `"enabled": true`). He asked specifically that switching it on be trivial.
3. **SharePoint: document the procedure, do not build it.** No admin rights on the FS tenant. `docs/SHAREPOINT.md` has the Graph recipe.
4. **Work-machine reality:** web-only Office, no PDF editor, no admin, no Gmail — **but github.com AND claude.ai both load from a Four Seasons machine**, so a link is a viable delivery path and no file-moving is needed. PDF is the work-facing format.

## ⚠️ THE Ch. 1702 FLAG — the most important thing in this file
Ryan floated auto-forwarding the brief from his **Rowan Risk Solutions** email to Four Seasons as a paper trail with future "cache." **This was flagged back as cutting against his own legal analysis** and he chose not to do it yet.
Full reasoning is in `docs/EMAIL.md` in the repo: [[guest-edition-proposal]] rests on **§1702.323**'s employee-employer exemption, and the hotel-owned model was chosen *specifically* to sit inside it. Branded daily delivery from a separate LLC creates a written record of exactly the fact pattern the exemption does not cover — and **automation turns one judgment call into 365 documented instances** before the counsel read that proposal logged as open item #2. "Not making money off it" addresses §1702.104's *for hire* language but not the entity question.
**Accepted alternative: the git repo is the better paper trail** — timestamped, hash-chained, authored commits, private until he chooses to show them. Also flagged: emailing the Guest Experience distro would unilaterally change the workflow Magee/Storck asked for (one-pager → **Overnight MOD** → internal distribution), and an external automated sender with daily attachments into an M365 tenant is a quarantine trigger. If email is ever switched on: **one named internal recipient, HTML in the body, attachments secondary.**

## SharePoint / Teams distribution — asked again 5 Sep 2026, findings recorded, **Ryan reviewing, not decided**
He asked whether the brief could auto-post to a SharePoint site or Teams on the FS network, or auto-forward to his work email which would then post it on-network. Findings:
- **SharePoint via Graph is a dead end without admin.** It needs an app registration and admin consent in the FS tenant. Egress reaches `graph.microsoft.com`, but a 401 he can never satisfy is still a wall.
- **⚠️ Office 365 connectors and Teams Incoming Webhooks were FULLY RETIRED on 22 May 2026.** The classic webhook recipe in `docs/SHAREPOINT.md` is dead — **do not offer it**. The replacement is a **Power Automate Workflow** ("Post to a channel when a webhook request is received"), which a **standard user can create with no tenant admin rights** on E1/E3/E5/F3, and which posts **on behalf of the user who created it** — so the post would carry Ryan's name.
- **The autoforward leg is the weakest link.** M365's outbound spam policy defaults to *Automatic – System-controlled*, which for anything but a long-established tenant means external forwarding is **off**, failing with NDR `5.7.520`, and **a standard user cannot override it**.
- **⚠️ The Ch. 1702 flag fires harder here than on email.** A scheduled push from an RRS sender into the FS tenant is documentary evidence of the *vendor* fact pattern the §1702.323 exemption does not cover, and automation makes it ~365 timestamped instances a year — all accruing before counsel reads the proposal (**open item #2, still open**). **The delivery path is not neutral plumbing; it is evidence about which model is operating.**
- **Recommended architecture if he proceeds: push nothing from Rowan, pull everything from inside.** Cloud job publishes to the private repo; nothing crosses the boundary; a Power Automate flow **Ryan owns, running as him on his FS licence** posts it. A post attributed to his FS account, sourced from a file he opened at work, is the *employee* fact pattern and looks like it in the audit log. Fetching an external URL needs the **premium HTTP action** and may hit DLP; the free fallback is the webhook carrying **a link, not a file**.
- **Cleanest option offered: he posts it himself.** github.com and claude.ai both load from an FS machine — open, download, drop in the library, ~30 seconds, zero ambiguity.
- **Whatever path: do not route around the Overnight MOD.** Magee/Storck asked for one-pager → MOD → internal distribution; auto-posting to a channel at 03:15 deletes the MOD's role. If automated, post to a channel only Ryan and the MOD watch — **never the Guest Experience distro**.
- **Cheap diagnostic he was given:** open Teams at work and see whether the **Workflows** app is available at all. If blocked, that settles it and says a lot about tenant posture.
- **Offered and not yet built:** `docs/DISTRIBUTION.md` in the repo capturing the above.

## ⚠️⚠️ THE DOCX — READ THIS BEFORE TOUCHING mkdocx.py
**The first native build shipped broken and Ryan caught it.** It was "verified" by counting Word tables and characters and **never rendered**. It came out at **2pp (DBS) and 10pp (FULL)** with the lead **shattered into one paragraph per bold phrase**.
- **Root cause: block/inline confusion.** The walker created a new Word paragraph for every `<b>`. **The rule: a Word paragraph corresponds to an HTML *block*; every inline descendant (`<b>`, `<em>`, `<span>`, bare text) belongs in the SAME paragraph as runs.**
- **CSS flex/grid rows have no whitespace in the source** — topbar, classline, strip rows, contact rows must get separators inserted explicitly or the text concatenates ("ATX Security Office**DTG** 030600").
- **`scripts/mkdocx.js` must run first.** The day-arc chart is drawn by JavaScript and does not exist in static HTML; LibreOffice and pandoc silently lose it. A DBS docx under ~40 KB means the chart was dropped. **`mkmap.js` likewise rasterises the FULL's map SVG** — without it the FULL docx has zero images and fails G12.
- **LibreOffice and pandoc both produce ZERO Word tables** from the CSS grids. The native build gives **7 (DBS) / 10–12 (FULL)** real tables and opens correctly in **Word Online**, the only Word Ryan has at work.
- **⚠️ `tblLayout:fixed` is IGNORED unless `w:tblGrid` is rewritten** (found 4 Sep). Setting `cell.width` + `autofit=False` alone does nothing — Word and LibreOffice lay out from `w:tblGrid`. `fix_widths()` must clear and rebuild the gridCols and set `w:tblW`. **Fixing this recovered so much dead vertical space that the FULL went from needing scale 0.86 to fitting 6pp at 1.07** — bigger type, same page count. It also honours the `width:NN%` on the source `<th>`s.
- **⚠️ On tables of ≥6 columns, never shade the status cell** — Word stretches the fill to full row height and a tall Watch Item row becomes a black slab. Colour the badge *text* instead. Shade only in narrow/short tables (the 5-chip band, the DBS watch rows).
- **Page counts differ by design: PDF 5pp/1pp, DOCX 6pp/1pp.** **`autotune.py` binary-searches the type scale to the target — never hand-pick a scale, it drifts.** Search range 0.60–1.30. Ed. 249 settled at **FULL 1.0703 / DBS 0.8543**.
- **LESSON, generalised: structure metrics are not appearance. Render every artifact and look at it before delivery.**

## ⚠️ THE PRINT-CSS LESSON (found 4 Sep, generalised from the `.qa` trap)
**Almost every block in the DBS hard-codes its `font-size` in the SCREEN css**, so `body{font-size}` in `@media print` moves almost nothing — a 6.85→6.55px body cut bought only ~0.67in. **Adding explicit print overrides for `.lead`, `.lead .focus`, `.craft .cl`, `.craft .q`, `.wi .r`, `.dv p`, `.out .d p`, `.ready p`, `.flag .t`, `.cell .lab/.chip/.tr` and `h3.dash` took the DBS from 2pp to 1pp and let the type be raised back up** — it ended more readable than it started. **Rule: when a print page overflows, grep the screen CSS for every hard-coded `font-size` in the overflowing region before touching `body`.**

## The gates — `scripts/verify.py`, G1–G12, 23 checks
All 23 pass on ed. 247, and six deliberately mutated copies were each caught. Notable:
- **G3** reads the heat flag from the **rendered `.lvl` badge, never prose** (prose legitimately says "flag goes Black" as a conditional) and excludes the Section 09 Tripwire row as hypothetical by construction. Both were false positives on the first run — **fix the gate, don't loosen it**. **⚠️ G3 must now accept Yellow**: ed. 249 stepped Red→Yellow at an index of 102°, the first flag change in six editions.
- **G2** WI age = prior + days elapsed. **G10** spelled-out day counts vs dated anchors. **G9** blocks retired framings but exempts text that quotes them in order to forbid them.
- **G12** DOCX page count, real-table floor, embedded image — added after the failure above.
- **⚠️ NEW GATE NEEDED (G13): unsupported comparatives.** Ed. 249's numeric audit caught three of Claude's *own* claims — "the eighth time", "the most chips this brief has carried", "the quietest stretch since ed. 245" — none sourced. **"first", "most", "highest", "nth time" need a source or they get cut.** The audit must cover superlatives, not just figures.

## ⚠️ OPEN — not yet done
- **The scheduled task has NOT been created.** Needs the repo URL and a fine-grained PAT (one repo, contents:write, 90-day expiry) — only Ryan can produce those. He was asked to send both in one message.
- **Fire time 08:15 UTC = 03:15 CDT** — after the CLI report (~02:20–02:40) and the NWS morning point product (~01:24–02:46). **⚠️ Ed. 249 ran at ~01:00–02:05 CDT and the CLI *final* had still not issued**, so the maximum was single-issuance. A 03:15 fire time avoids this; a manual run before ~02:40 will not.
- **⚠️⚠️ DST: on 1 Nov 2026 change the cron to `15 9 * * *`.** `15 8` becomes 02:15 CST, *before* the morning products issue.
- A **watchdog at 09:15 UTC (04:15 CT)** should check today's edition exists on `main`.
- PAT lives in the trigger prompt; the offered alternative (Drive file read via the connector) was not built because **connector availability inside a scheduled run is untested**. Test on the first live run.
- **⚠️ The repo does not yet hold the edition HTML.** Eds. 246/247 exist only as PDF/DOCX and had to be rebuilt from ed. 245 — see [[ed249-state]]. **Every edition's HTML must be committed daily or that rebuild cost recurs.**

## Token economics (measured)
Ed. 247 cost **~323k tokens** end to end against a 15M budget → **~9.7M/month**, leaving ~35%. Tuned steady state estimated **190–220k/edition ≈ 5.7–6.6M/month**, leaving 56–62%. Recoverable gap is one-time discovery (template learning ~35k, page-fit search ~30k, DOCX pipeline ~10k). **The dominant cost is context re-transmission** — a 45-call session pays for its own history ~45 times — so batching calls beats trimming steps. **Ed. 249, built from ed. 248 as a base with the pipeline already written, was materially cheaper than the two rebuild editions before it.**
