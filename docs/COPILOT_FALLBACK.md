# 06 — THE COPILOT FALLBACK
### Producing the Daybreak Brief with Microsoft 365 Copilot on a locked network

**Use this when you cannot reach Claude, the CLI, or XEN0 — but you can reach Copilot.**
It will not produce the six-file package. It will produce **a true, on-time, readable brief**,
which is the thing that actually matters at 0600.

---

## 1. What Copilot can and cannot do here

```
        CAN                                CANNOT
  ┌──────────────────────────┐   ┌────────────────────────────────┐
  │ Draft prose in the house │   │ Reliably fetch a specific URL  │
  │ voice from facts you give│   │ Read api.weather.gov JSON      │
  │ Format a Word document   │   │ Tell you a source FAILED       │
  │ Summarise pasted text    │   │ Hold state between sessions    │
  │ Build a table            │   │ Render the HTML/PDF template   │
  │ Check your arithmetic    │   │ Autotune DOCX to a page count  │
  └──────────────────────────┘   └────────────────────────────────┘
```

**The one that will hurt you is in the right-hand column: Copilot does not report failure.**
Ask it for yesterday's Camp Mabry maximum and it will give you a number. It may be from a
different day, a different station, a news article, or its own inference — and it will read
exactly like the true one. **Claude's whole G13 gate exists because a silent gap is worse
than a loud one. Copilot has no such gate, so you are the gate.**

---

## 2. The division of labour that works

```
  YOU (browser)          →   COPILOT (chat)        →   COPILOT (in Word)
  open 6 URLs                assemble + draft          format + finish
  copy/paste raw text        the prose sections        the document
  ~10 minutes                ~5 minutes                ~5 minutes
```

**Paste the raw text in yourself.** This is the single change that turns Copilot from
unreliable to genuinely useful. You are removing the one thing it is bad at (retrieval)
and keeping the two it is good at (synthesis and formatting).

### The six URLs to open and copy (in this order)

| # | Open this | Copy |
|---|---|---|
| 1 | `https://forecast.weather.gov/MapClick.php?lat=30.27&lon=-97.74` | The worded forecast column — today, tonight, next 2 days |
| 2 | `https://api.weather.gov/alerts/active?point=30.27,-97.74` | The whole page (if it says `"features": []` there are **no alerts**) |
| 3 | `https://forecast.weather.gov/product.php?site=EWX&issuedby=ATT&product=CLI` | Yesterday's MAXIMUM, MINIMUM and PRECIPITATION lines |
| 4 | `https://www.austintexas.gov/news` **and** `https://www.austintexas.gov/police/news` | The top 5 headlines **with dates**, from **each** feed separately |
| 5 | Moody Center, ACL Live and **3TEN** calendars | Anything in the next 3 days, plus the next UT home game |
| 6 | `https://texassports.com/sports/football/schedule` | Next home game: opponent, date, **kickoff time** |

> **If a page will not load, write `NOT RETRIEVED` for it.** Do not skip it silently and do
> not ask Copilot to fill it in. A named gap is a finished brief; a guessed number is a
> problem you will find out about in front of the GM.

---

## 3. PROMPT 1 — the fact pack (paste into Copilot chat)

> Copy everything in the box. Replace the `«...»` parts. Paste your copied source text
> underneath where it says RAW SOURCE TEXT.

```
You are helping me assemble a daily internal security awareness brief for a hotel in
downtown Austin, Texas. Today is «DATE». This is edition ATX-DB-2026-«NUMBER».

I am pasting RAW SOURCE TEXT that I copied myself from official pages. Work ONLY from
what I paste. This is the most important instruction in this prompt:

RULES — follow these exactly:
1. Do NOT use your own knowledge, memory, or web search for any number, date, name or
   time. Every figure in your output must appear in the text I pasted.
2. If something I need is NOT in the pasted text, output the literal words
   "NOT RETRIEVED THIS PASS" for it. Never estimate, never infer, never fill a gap.
   A missing figure is an acceptable answer. An invented one is not.
3. Distinguish OBSERVED (already happened, past tense) from FORECAST (has not happened).
   Never describe a forecast as though it were measured.
4. At the end, output a SOURCE LEDGER table listing every item I asked for, marked
   RETRIEVED or NOT RETRIEVED. I need to see the gaps, not have them hidden.
5. Do not use the words "approximately", "around" or "roughly" in front of a number
   unless the source did. Quote the source's own precision.

Produce these sections, in this order:

A. WEATHER — today's high, low, heat index, chance of rain; tonight's low; the next two
   days. Quote the product's issuance time if it appears in the text.
   THEN: check the heat index against 108°F, which is the Heat Advisory criterion here.
   Tell me explicitly whether it is above, below, or within 3 degrees of that line.
B. ADVISORIES — are any watches/warnings/advisories in force? If the alerts text shows an
   empty features list, say "None in effect" and say that is what the feed reported.
C. OBSERVED YESTERDAY — maximum, minimum, precipitation, with the time of the maximum.
D. LOCAL — the most recent items on EACH City feed, with dates, listed separately. Tell me
   the date of the most recent INCIDENT item specifically, which is different from the most
   recent posting of any kind.
E. EVENTS — anything at a downtown venue in the next 3 days. Then the next UT home game:
   opponent, date and kickoff time. If every venue is dark, say so plainly.
F. SOURCE LEDGER — the table from rule 4.

RAW SOURCE TEXT:
«paste everything you copied here, with a line naming each source above its text»
```

**Read the SOURCE LEDGER before you read anything else.** If a row you pasted text for
shows NOT RETRIEVED, Copilot could not find it in your paste — check you copied the right
part. If a row shows RETRIEVED but you never pasted it, **it made it up** — start again.

---

## 4. PROMPT 2 — the brief itself

```
Using ONLY the fact pack you just produced, write the daily brief. Keep every rule from
my last message, especially: no figure that is not in the fact pack, and print
"not verified this pass" wherever the ledger said NOT RETRIEVED.

Structure and voice:
- Open with a BOTTOM LINE of 4–6 sentences. Lead with what CHANGED since yesterday, not
  with a list of conditions. Plain declarative sentences. No throat-clearing.
- Then FIVE status chips, one line each, with a level from: Calm, Attentive, Elevated,
  High, Severe — for: Neighborhood & Street / Public Gatherings / Weather & Storms /
  Traffic & Arrivals / Utilities & Grid. Say which way each moved and WHY in one clause.
- Then WHAT TODAY ASKS OF YOU — one line each for: Front Office, Valet & Front Drive,
  Housekeeping, Food & Beverage, Banquets, Engineering, Spa & Fitness, Security.
  Each line must contain an ACTION, not an observation.
- Then IF A GUEST ASKS — four Q&As in the voice of a concierge speaking to a guest.
  Warm, brief, no jargon, no numbers the guest did not ask for.
- Close with SOURCES & CONFIDENCE: what was verified, what was not, and one sentence
  saying how confident I should be and why.

The Exterior Team Heat Flag bands are: Green normal · Yellow index 91–102 ·
Red index 103–115 · Black heat advisory in force or index 115+.
State the flag and say plainly whether an advisory is in effect. Those are two different
things and staff conflate them.

Tone: written for people about to start a 12-hour shift. Calm, specific, no alarm, no
padding. Never say "stay vigilant" or "monitor the situation" — say what to do instead.
```

---

## 5. PROMPT 3 — format it (Copilot **in Word**)

Open a blank Word document → Copilot → paste:

```
Format the text I am about to paste as a one-page internal briefing document.
- Title block: "DAYBREAK BRIEF", then the date and edition number, then the line
  "Internal — Not For Guest Distribution".
- The five status lines as a single-row table with five columns, each cell showing the
  area name above its level.
- Each named section as a bold heading, 11pt body, tight spacing.
- Keep it to ONE page: reduce body text to 9pt and tighten margins to 0.5" if needed.
- Do not add any content, any commentary, or any wording of your own.
```

Then **File → Export → Create PDF/XPS**. That is your distributable file.

---

## 6. The five-minute verification, before you send it

Copilot will not do this for you. Neither will anyone else.

| ✓ | Check | Why it is on this list |
|---|---|---|
| ☐ | **Every number traces to text you pasted** | The failure mode is a confident invented figure |
| ☐ | **The date on every source is the date you expect** | Annual events and weather stories recur with near-identical wording; a 2023 article reads as current |
| ☐ | **Observed vs forecast is right** | "Yesterday hit 102°" and "yesterday was forecast at 102°" are different claims |
| ☐ | **Gaps are printed, not omitted** | If a source failed, the brief must SAY it failed |
| ☐ | **Heat index vs the 108° line** | If it is within 3°, re-read a fresh forecast before you publish |
| ☐ | **Both City feeds checked separately** | The police feed carries items the general feed does not |
| ☐ | **The UT home game** | This is the miss that started all of it. Check the list, do not check your memory |
| ☐ | **No superlative without a basis** | "first", "most", "highest", "worst" — cut it or source it |

---

## 7. Copilot's specific failure modes with this product

| It will… | Because | Do this |
|---|---|---|
| Give a plausible temperature for any day you ask about | It is a language model with weather in its training data | Only accept figures from your pasted text |
| Say "no significant incidents" without checking | It reads absence of information as absence of events | Make it name the date of the last incident item |
| Merge the two City feeds into one list | They look like the same site | Paste them under separate headings and say so |
| Smooth over a contradiction between two sources | It is trained to produce a coherent answer | Tell it to print both and reconcile neither |
| Lose the previous edition's watch-item ages | No memory between chats | **Paste yesterday's watch-item list every day** |
| Round a heat index | Fluency over precision | Rule 5 in Prompt 1 |
| Drop a caveat when you ask it to shorten | Caveats look like padding | Re-check every trimmed section |

---

## 8. Carrying state — the thing Copilot cannot do at all

There is no `LATEST_STATE.md` in Copilot. **You are the state file.**

Keep a single Word or OneNote page, updated each morning, and **paste it into every
chat**:

```
CARRY FORWARD — as of ed. «N»
Watch items and their ages:   WI-05 Day «n» · WI-06 Day «n» · WI-10 Day «n» · WI-11 Day «n»
Chips as they closed:         Neighborhood «x» · Gatherings «x» · Weather «x» · Traffic «x» · Utilities «x»
Heat flag:                    «colour», «n» consecutive days
Open local cases and ages:    «...»
Corrections not to repeat:    «...»
Next known big day:           «...»
```

**Ages step by exactly one each edition.** If you skip a day, say the item was not checked
rather than incrementing silently.

---

## 9. When to stop using Copilot and go back

Copilot is the **fallback**, not the method. Go back to the CLI the moment you can, because:

- `daybreak fetch` reaches sources Copilot cannot, and **tells you when it fails**
- G13 makes coverage a loop instead of a judgement
- G14 catches a forecast number sitting on a decision threshold
- `build --degraded` gives a facts-only brief with **no model at all** — which, on a truly
  bad morning, is more reliable than any chatbot

**And note the ranking:** a degraded machine-built brief with printed gaps beats a
polished Copilot brief with a confident wrong number. **Fluency is not accuracy, and this
product's whole value is that people can act on it without checking it.**
