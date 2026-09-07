# IT REQUEST #2 — network reachability for the daily brief

**Send this only after you have tried the two tests at the bottom yourself.** If
`claude.ai` already loads from a hotel machine, you do not need this email at all —
send `IT_REQUEST.md` (the SharePoint one) and nothing else.

Paste the section between the rules. Everything after it is your own reference.

---

**Subject:** Two questions about site access for the daily security brief

Hi [Name],

Following on from my note about a SharePoint location for the daily awareness brief —
I have two quick questions about what's reachable from a hotel machine. Neither is a
request for a permission or a role; I'm trying to find out which distribution method
will actually work here before I ask you to set anything up.

**1. Is `claude.ai` reachable from the property network?**

I draft the brief with an AI assistant on my own licence, on my own equipment. The
finished brief can be published to a private page there, and the team would open the
same link each morning. That only works if the domain resolves from a hotel machine.

If it's blocked, please just tell me — I'll use the SharePoint folder instead and drop
this idea. If it's blocked only by category (an "AI tools" filter, say) and an
allowlist entry for `claude.ai` is straightforward, that would be useful, but it is
not important enough to argue for.

**2. Is `drive.google.com` blocked deliberately?**

It doesn't load from here. I'd assumed that was policy rather than a fault, but I want
to confirm before I stop treating it as an option. Not asking for it to be opened.

**Context, so the questions make sense:**

- The brief is internal operational awareness only — weather, local events, traffic,
  neighbourhood conditions, a short readiness item.
- **No guest data, no PII, no cardholder data, nothing from any hotel system.**
- Sources are all public: National Weather Service, City of Austin, APD public
  releases, venue calendars, ERCOT.
- It's marked *Internal — Not For Guest Distribution*.
- Nothing I'm describing sends anything **into** the hotel network. It's a page staff
  would read, in a browser, the same way they'd read a news site.

**What I am not asking for:** no admin role, no firewall change beyond a possible
single-domain allowlist entry, no inbound access, no software installed on hotel
equipment, no mailbox rules.

If it's easier to answer in person, I'm on property most mornings.

Thanks,
Ryan Pair
ATX Security Office

---

## YOUR REFERENCE

### Run these two tests BEFORE sending. They may make the email unnecessary.

| # | Test | How | If it fails |
|---|---|---|---|
| 1 | **Does `claude.ai` load on the hotel network?** | Open it on a hotel machine | Send the email. This is the gate on the whole artifact route. |
| 2 | **Does the shared link open with no sign-in?** | Publish → Share → *anyone with the link* → copy → open in a private window | Sharing wasn't enabled, or artifacts require an account. Either way, staff-wide distribution needs SharePoint. |

**Test 2 is free and takes two minutes — do it first.** If the link needs a Claude
account, question 1 stops mattering and the SharePoint ask becomes the only route.

### Why these are framed as questions, not requests
An allowlist request lands on someone's risk register. A question about whether a
domain resolves is a two-word answer. You want the answer, not the ticket — and if
the answer is "blocked, and staying blocked", you have lost nothing and you know to
put the effort into `IT_REQUEST.md` instead.

### What NOT to ask for here
- Do not ask for an exception to an AI-tools policy. If one exists, that is a
  conversation for the GM and Legal, not the help desk.
- Do not ask for anything that lets an outside system write **into** the tenant.
  That's the vendor-integration pattern, and it is the fact pattern your
  §1702.323 employee-exemption position depends on not establishing.
- Do not mention automation or scheduling in this email. It invites the question
  "what software is running where?", which is a much longer conversation than
  "does this website load?"

### If both routes are refused
The fallback is real and it works: the brief is produced on your own equipment, the
six files land in a folder, and a named deputy has `DAYBREAK_KB` on XEN0 with the
runbook and the degraded mode. Distribution stays manual. That is worse, but it is
not a failure — it is where you already are today.
