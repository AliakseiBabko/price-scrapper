# Intake pipeline lessons

These postmortems preserve the evidence behind the short operative rules in
the parent skill. They are reference material, not additional pipeline steps.

## Background-agent dispatch

On 2026-08-17 a dispatched batch agent reported completion while making no
real file changes and claimed it had launched another background agent. The
untracked process continued writing for roughly 40 minutes, outside the
orchestrator's visible control, causing a concurrent-writer collision: two
CSV run IDs collided under the old sequential scheme and a wiki citation
pointed to a differently named file. Later that day run IDs were changed to
source-keyed IDs, but that does not remove the need to verify `git status`,
CSV progress, archive citations, and now the per-video status JSON. Another
multi-video dispatch repeatedly reported completion at spacing waits; the
same agent had to be resumed six times for one seven-video chunk. This is why
chunks stay small and progress is checked from files rather than prose.

## Negation-routing incident

During the 2026-08-18 routing pass, comparing a new claim against an existing
wiki page exposed a reversed extraction. A transcript used the contrast form
`не такую... а...` (“not the X kind, rather Y”); the extraction recorded the
preference backwards as “prefer tube-based lubricant,” while the source said
the opposite. The store's corroboration note then incorrectly said two
sources agreed. Re-reading the original transcript before calling a claim
corroborating, and flagging ambiguous contrast/negation as uncertain, is the
required safeguard.

## WebFetch tabs incident

On 2026-08-10 a company page was checked with a WebFetch-style summarization
read. Everything returned was accurate, but an entire tabbed section of
concrete content was absent because only the default tab was visible to the
read. The substantive material lived in the DOM behind tab clicks, alongside
accordions, expanders, and modal-triggered sections. A real rendered browser
must therefore be used for evidence, with hidden sections opened and the
result saved as an evidence file; a summarization fetch is acceptable only
for a quick non-evidentiary question.
