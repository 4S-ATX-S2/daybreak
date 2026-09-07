# Project Memory — 4SDAB_Design

- [Ed. 251 state](ed251_state.md) — **READ BEFORE ed. 252.** The Black-flag tripwire resolved DOWN to 105°; `api.weather.gov` replaced the rendered NWS pages and recovered four dead sources (21/23); Gatherings hit Calm; the superlative sweep caught a false "first Calm chip" claim.
- [Ed. 250 state](ed250_state.md) — superseded. Kept for the **107/109 threshold correction** (rule 12 / gate G14) and the four-dead-source pass.
- [Automation](automation.md) — **READ BEFORE CHANGING HOW EDITIONS ARE PRODUCED OR DELIVERED.** Cloud-native repo, verified egress, the gates, the native-DOCX pipeline, the Ch. 1702 flag, and the SharePoint/Teams findings.
- [Verification discipline](verification_discipline.md) — the **12** hard rules plus the superlative sweep; every one written from a real published error.
- [Daybreak Brief workflow](daybreak_brief.md) — how to produce the brief by hand (format, edition numbering, sources, page-fit, render pipeline).
- [DBS one-pager](dbs_onepager.md) — the wider-distribution 1PG: eight-division row, Readiness rotation, the `.qa` page-fit trap.
- [Ed. 249 state](ed249_state.md) — superseded; kept for the **UT-game miss**, the four review-pass corrections, and the `.qa`/`w:tblGrid` lessons.
- [Guest Edition proposal](guest_edition_proposal.md) — the commercial pitch; pricing, the §1702.323 exemption the model rests on, the open counsel question.
- [Ed. 247 state](ed247_state.md) · [Ed. 246 state](ed246_state.md) — superseded; kept for the heat-run history and the correction record.

## The tooling (as of ed. 251)
**`daybreak` CLI — the pipeline.** `fetch` → `draft` → `build` → `publish`, four stages run independently. **Only `draft` needs a model**; `fetch` + `build --degraded` produce a facts-only edition with no model, no API key and no license. Standard library only, no `pip install`. **Gates: G13 source coverage (PASS / DEGRADED / PARTIAL / FAIL) and G14 threshold re-read.**
**⚠️ Use `api.weather.gov`, NOT `forecast.weather.gov` product pages** — the rendered pages lost four Tier-1 sources for a whole edition; the service endpoints answered all four first try. **When a source fails repeatedly, question the ROUTE before the source.**

## Where things live
- **XEN0: `00_TheSea/DAYBREAK_KB/`** — the working knowledge base + `cli/` + `editions/`.
- **AI_Mobile (Sharge): `DAYBREAK_BRIEF/`** — **the portable copy, organized for a cold start on any machine.** `START_HERE.md` at the root routes by situation; `1_RUN/` do it today · `2_METHOD/` why · `3_STATE/` carry-forward (**includes a copy of this whole memory folder**) · `4_BUILD/` templates+scripts · `5_EDITIONS/` archive · `6_ADMIN/` IT and distribution. **Verified running live from the drive.**
- **Stable team web URL** in `config/artifact.json` — **republish to it; publishing without it makes a new artifact and the bookmark dies.** Note: viewers currently see a **pinned earlier version**, which needs changing in the share menu.
