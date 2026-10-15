# Report template

Fill in every section. When a section has nothing to report, write `none` instead of deleting it, so a reader can tell the check was done.

## Rules for the whole report

- Each claim cites the evidence IDs and locators that support that specific claim. A citation that supports a nearby claim, or the topic in general, doesn't count.
- A source stating a fact doesn't make the fact true. Write what the source said, and add independent evidence before stating the fact yourself.
- Qualitative findings, fractions, and counts stay inside the observed sample and name its unit, for example "3 of 12 inspected comments". Don't turn them into audience percentages.
- A convenience sample, engagement counts (likes, views, shares), or a repeated post doesn't support a claim about audience prevalence, consensus, or a trend across a platform.
- Discovery-only and inaccessible records never support a finding. They appear only in counts, limits, and unanswered questions.

## Layout

```markdown
# Social evidence report: <question>

Status: complete | partial (<what is missing and why>)
Prepared: <date and time>

## Protocol

- Question: <the research question>
- Platforms: <platforms and exports in scope>
- Date range: <start> to <end>, by publication time
- Selection method: <how records were chosen, such as "first 20 results for query X, sorted by recent">
- Unit of analysis: <post, comment, video, author, or other>
- Maximum sample: <cap per platform and overall>
- Stopping rule: <when collection stops>
- Protocol changes: none | <what changed, when, and why>

## Collection counts

| Stage | Count | Unit | Notes |
| --- | --- | --- | --- |
| Discovered | | sources | <discovery-only records: search cards, snippets, and supplied URLs> |
| Inspected | | parts | <inspected parts, and the number of distinct sources (`source_id`) they come from> |
| Excluded | | | <each exclusion reason with its count> |
| Access gaps | | | <each gap type with its count> |
| Duplicate groups | | groups | <members per group; repeated content counted once> |

Overlap: <explain how the rows relate, using `discovered_via` and `source_id`, for example "31 of the 40 discovered sources were opened, giving 58 inspected parts. 4 export rows were inspected without a discovery record.">

## Findings

| # | Claim | Evidence IDs and locators | What the source said | Researcher interpretation | Limitation |
| --- | --- | --- | --- | --- | --- |
| 1 | | E015 (comment id 88213) | | | |

## Attribution notes

<Who said what: post authors, commenters, and reposting authors, kept apart from the researcher's conclusions.>

## Duplicate groups

| Group | Original | Reposts, cross-posts, captures | Counted as | Uncertain |
| --- | --- | --- | --- | --- |
| D1 | E004 | E009, E011 | one original statement, plus E011's added commentary as a separate statement | no |

## Access and collection limits

- <Login gates, deleted or unavailable content, missing export fields, rate limits, incomplete comments or media, with record IDs>
- <Empty searches: the query, platform, and time, recorded as a collection limit, not as evidence of no discussion>
- <Sampling limits: what the sample can and can't represent>

## Unanswered questions

- <Each part of the question the evidence couldn't answer, and what evidence would answer it>

## Evidence records

<All records, in the format from evidence-record.md, including discovery-only and inaccessible ones.>
```

## Writing the claim table

- **Claim** is the researcher's sentence, worded to stay inside the evidence, such as "Two of the five inspected creator captions mention battery life."
- **What the source said** quotes or closely paraphrases the source, attributed to its author, such as "@trailcam_dana wrote that the battery lasted two days."
- **Researcher interpretation** is your reading of the material, labeled as yours. Leave it as `none` when the claim is purely descriptive.
- **Limitation** names what the claim can't show, such as "Caption only. The attached video wasn't inspected."

## Marking a partial report

Set `Status: partial` when the evidence the question needs is unavailable, for example when the key platform is behind a login gate, or when the stopping rule ended collection before the records the question needs were inspected. Keep the findings that the available evidence supports, and list what is missing under unanswered questions. Don't fill gaps with discovery-only records, guesses, or general knowledge.
