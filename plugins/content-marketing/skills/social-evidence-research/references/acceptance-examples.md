# Acceptance examples

Each example gives compact input records and the result the method must produce. A reviewer can check them by reading the rules in `SKILL.md`, `evidence-record.md`, and `report-template.md`, with no accounts, browsing, or paid services. Records show only the fields the example needs. All handles and URLs are made up.

## Summary

| Input | Expected result |
| --- | --- |
| One inspected caption, three search cards, and an unwatched attached video. | Only the caption supports claims about the post's text. The cards remain discovery-only, and the video's contents remain unknown. |
| An original post, two reposts, and a disagreeing comment. | The repeated original counts once as support. The comment is attributed to its commenter and does not change what the post author said. |
| Three supportive comments among twelve inspected comments selected by a stated method. | The report can say "3 of 12 inspected comments expressed support," with citations and sample limits. It cannot infer that 25% of the audience supports the topic. |
| A blocked source and an empty search result. | Both appear in the access and collection limits. The report makes no claim that the topic has no discussion. |
| A transcript read, with the video unwatched. | Claims cover the transcript text only. What the video shows stays unknown. |
| An export with a capture date and origin. | Claims cite the export as a capture from that date, never as a live check. |
| A repost with added commentary. | The original counts once. The added commentary is a separate statement by the reposting author. |
| A source stating a fact. | The report says the source stated it. It doesn't present the fact as true. |
| A harness without browsing, given only URLs. | Every URL is discovery-only, no finding is made, and the report is partial. |
| A draft report to audit. | Each unsupported claim is flagged with the rule it breaks, and no replacement evidence is invented. |

## 1. Caption, search cards, and an unwatched video

Input:

| ID | Part | State | Author | Content |
| --- | --- | --- | --- | --- |
| E001 | caption | inspected | @hike_lena | "Finally a headlamp that doesn't die halfway up." |
| E002 | post-text | discovery-only | @gearnotes | Search card snippet: "honest review of the..." |
| E003 | post-text | discovery-only | @summit_jo | Search card snippet: "returned mine after..." |
| E004 | post-text | discovery-only | unknown | Search card with no snippet |
| E005 | video-interval | discovery-only | @hike_lena | Video attached to E001's post, not watched |

Expected result:

- Only E001 supports a claim about the post's text, such as "@hike_lena's caption says the headlamp 'doesn't die halfway up.'" Reading that as praise for battery life is an interpretation, so it goes in the interpretation column.
- E002 to E004 count under Discovered and support no finding. "Returned mine" in E003 is a snippet, so the report can't say @summit_jo returned the product.
- The video's contents are unknown. The report lists E005 under unanswered questions and makes no claim about what the video shows.

## 2. Original post, two reposts, and a disagreeing comment

Input:

| ID | Part | State | Author | Content | Duplicate |
| --- | --- | --- | --- | --- | --- |
| E010 | post-text | inspected | @lumen_labs | "Our new lamp runs 40 hours on one charge." | D1, original |
| E011 | post-text | inspected | @deals_daily | Same text, no added words | D1, repost of E010 |
| E012 | post-text | inspected | @lamp_fan | Same text, no added words | D1, repost of E010 |
| E013 | comment | inspected | @k_ramos | "Mine got 22 hours, not 40." (on E010's post) | none |

Expected result:

- Group D1 counts once as support for "@lumen_labs says the lamp runs 40 hours", not as three independent sources. The collection counts still list E010, E011, and E012 as three inspected sources in one duplicate group.
- The duplicate groups table shows E010 as the original and keeps the E011 and E012 references.
- E013 is attributed to @k_ramos. It doesn't change what @lumen_labs said, and the report shows the two statements separately.

## 3. Supportive comments in a bounded sample

Protocol: the first 12 top-level comments under one post, sorted by newest, inspected on 2026-10-14. The unit of analysis is the comment.

Input: E020 to E031, twelve inspected comments. E021, E025, and E030 express support. The post shows a count of 340 comments, and the page doesn't say how many of them are replies.

Expected result:

- The report can say "3 of 12 inspected comments expressed support (E021, E025, E030)", with the selection method in the limitation column.
- It can't say "25% of the audience supports the product" or "most commenters are positive".
- The limits section says 12 top-level comments were inspected, and the post shows 340 comments that may include replies. The number of top-level comments that weren't inspected is `unknown`, so the report doesn't give one.

## 4. A blocked source and an empty search

Input:

| ID | Part | State | Detail |
| --- | --- | --- | --- |
| E040 | post-text | inaccessible | `access_gap: login-gate`, community page requires sign-in |
| none | search | none | Query "lumen lamp recall" on a video platform returned 0 results on 2026-10-14 at 16:00Z |

Expected result:

- E040 is listed in access and collection limits, with its gap type.
- The empty search is listed as a collection limit, with the query, platform, and time.
- The report doesn't say "nobody is discussing a recall". If the recall question depends on these sources, the status is partial and the question stays unanswered.

## 5. Transcript read, video unwatched

Input:

| ID | Part | State | Author | Content |
| --- | --- | --- | --- | --- |
| E050 | transcript | inspected | @gearnotes | Auto-generated transcript: "It survived the drop test." |
| E051 | video-interval | discovery-only | @gearnotes | Video not watched |

Expected result:

- The report can say "The auto-generated transcript of @gearnotes' video includes the line 'It survived the drop test.'"
- It can't say the video shows a drop test or that the lamp survived one. The limitation column says the video wasn't watched and the transcript was auto-generated.

## 6. An export, not a live check

Input: E060 is an `export-row` from `community-posts.csv`, row 17, captured 2026-10-01T09:00Z. Its origin is "community moderator's export, supplied by the user". The user asks whether the post is still up.

Expected result:

- Claims based on E060 read "As of the export captured on 2026-10-01, the post said ...".
- Whether the post is still up today is an unanswered question, unless someone inspects the live page and records it as a new record.

## 7. A repost with added commentary

Input:

| ID | Part | State | Author | Content | Duplicate |
| --- | --- | --- | --- | --- | --- |
| E070 | post-text | inspected | @lumen_labs | "Price drops to $199 next week." | D2, original |
| E071 | post-text | inspected | @skeptic_sam | Repost of E070, adding: "Doubt it, they said the same in May." | D2, repost of E070 |

Expected result:

- The repeated text counts once, as @lumen_labs' statement.
- "Doubt it, they said the same in May" is a separate statement by @skeptic_sam. It is not a second source for the price drop, and it is not something @lumen_labs said.

## 8. A source stating a fact

Input: E080 is inspected `post-text` by @tech_watch: "The recall covers every unit sold before March."

Expected result:

- The claim table says "@tech_watch stated that the recall covers every unit sold before March", citing E080.
- The report doesn't state the recall's scope as fact. The limitation column says the statement wasn't checked against an independent source, such as the official recall notice.

## 9. No browsing, only URLs

Input: the user supplies five post URLs. The harness can't open web pages, and the user has no exports.

Expected result:

- Five discovery-only records, one per URL, each with the URL as `source_locator` and `capture_method: supplied-url`.
- Counts show Discovered 5 and Inspected 0. The findings table is empty.
- Status is partial. The report asks for exports or captured copies of the posts.

## 10. Auditing a draft report

Input: a draft report says "Most users love the lamp" and cites three search result snippets. It says "no one mentions overheating" and cites one search with no results. It quotes a comment as the brand's own statement.

Expected result:

- "Most users love the lamp": flagged twice. Its citations are discovery-only, and it makes a prevalence claim with no defined sample.
- "No one mentions overheating": flagged, because an empty search is a collection limit, not evidence of absence.
- The quoted comment: flagged as misattributed. The commenter said it, not the brand.
- The audit doesn't invent replacement sources. It lists what evidence each claim would need.
