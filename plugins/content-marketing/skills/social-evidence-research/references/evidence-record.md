# Evidence record

Each evidence record describes one part of one source and what the researcher did with it. Make a new record for every part you discover, inspect, or fail to reach. A post with a caption, two images, and five comments you read becomes at least eight records, not one.

Write `unknown` for any value you can't determine. Don't leave a field blank, and don't guess.

## Fields

| Field | What to record |
| --- | --- |
| `id` | A stable ID, such as `E014`. Never reuse or renumber an ID, because the claim table points to it. |
| `source_id` | A stable ID for the source this part belongs to, such as `S004`: one post with its caption, media, and comments, one video, one thread, or one export record. Every part of the same source shares it. A repost is its own source. |
| `platform` | The platform name, or `export` plus the platform when the record comes from a file. |
| `source_locator` | The source URL, or the export record locator: file name plus row number or record ID. |
| `discovered_via` | The ID of the discovery-only record that led you to this source, `supplied` when the user gave you the material, or `none`. Keep the discovery-only record after you open the source, so the path from discovery to inspection stays visible. |
| `source_author` | The author of this part: the post author for post parts, or the commenter for a comment. |
| `parent_id` | For a reply, the ID of the comment it replies to. Otherwise `none`. `source_id` already ties a part to its source. |
| `published_at` | Publication time shown by the source, with time zone, or `unknown`. |
| `observed_at` | When you inspected the part live, or the capture time of the export or captured file. |
| `capture_method` | `live-view`, `export`, `user-capture` (a screenshot or saved file the user supplied), `search-result`, or `supplied-url` (a URL the user gave that you haven't opened). |
| `export_origin` | For exports and captures, who produced the file and how, such as "account owner's data download". Otherwise `not an export`. |
| `inspected_part` | One value from the inspected-part list below. |
| `evidence_state` | `discovery-only`, `inspected`, or `inaccessible`. See the definitions below. |
| `excerpt_or_observation` | For text, a short exact quote. For images, audio, or video, a description limited to what you saw or heard in the inspected part. |
| `locator` | The precise place inside the source: comment ID, file row, image number, or media time range such as `01:10 to 01:40`. |
| `duplicate_group` | A group ID such as `D3` when the content repeats another record, or `none`. |
| `duplicate_role` | `original`, `repost`, `cross-post`, or `repeated-capture`, or `none` when there is no group. |
| `original_ref` | For a repost, cross-post, or repeated capture, the ID or locator of the original. Otherwise `none`. |
| `duplicate_uncertain` | `yes` when the grouping is likely but not confirmed, otherwise `no`. |
| `access_gap` | `none`, `login-gate`, `paywall`, `deleted`, `unavailable`, `rate-limited`, `missing-field`, `incomplete`, or `other` (describe the gap in `notes`, such as a region or age gate). |
| `exclusion` | `none`, or the reason the record was left out of the analysis, such as "outside date range". |
| `notes` | Anything else a reviewer needs, such as "auto-generated transcript". |

## Evidence states

- **discovery-only**: you saw the record only as a search result, card, snippet, preview, unopened URL, or an attachment you didn't open or play. It can guide follow-up. It can't support a claim about the source's content.
- **inspected**: you examined this part itself, live or in an export or capture. It supports claims about this part only.
- **inaccessible**: you tried to examine this part and couldn't. Fill in `access_gap`. It supports no content claim, and it belongs in the access and collection limits section of the report.

## Inspected-part list

| Value | Supports claims about | Doesn't establish |
| --- | --- | --- |
| `post-text` | The words of the post body | Comments, media, or the author's wider views |
| `caption` | The caption text | What any image, audio, or video shows |
| `comment` | One comment, attributed to its commenter | What the post author said or believes |
| `profile` | What the profile page showed at `observed_at` | Anything about posts you didn't open |
| `image-N` | Image number N, as seen | Other images in the same post |
| `video-interval` | The watched time range, given in `locator` | Unwatched parts of the video |
| `audio-interval` | The listened time range, given in `locator` | Unheard parts of the audio |
| `transcript` | The transcript text, noting whether it was auto-generated | What the video shows, or speech the transcript missed |
| `export-row` | The content of that row as of the capture time | The current live state of the page |

A record for a whole page with no part named isn't valid. If you only opened the page, record the parts you actually examined and leave the rest as discovery-only or unrecorded. Use `source_id` to group the parts of one source.

## Examples

A caption read in an export, from a post whose attached video wasn't watched:

```yaml
id: E007
source_id: S003
platform: export (video platform)
source_locator: creator-posts-2026-10-01.csv, row 42
discovered_via: supplied
source_author: "@trailcam_dana"
parent_id: none
published_at: 2026-09-28T14:03Z
observed_at: 2026-10-01T09:15Z (export capture time)
capture_method: export
export_origin: account owner's data download, supplied by the user
inspected_part: caption
evidence_state: inspected
excerpt_or_observation: "Battery lasted two full days on the trail."
locator: row 42, column caption
duplicate_group: none
duplicate_role: none
original_ref: none
duplicate_uncertain: no
access_gap: none
exclusion: none
notes: The row links a video file that was not supplied. See E008.
```

The same post's video, which couldn't be examined:

```yaml
id: E008
source_id: S003
platform: export (video platform)
source_locator: creator-posts-2026-10-01.csv, row 42
discovered_via: supplied
source_author: "@trailcam_dana"
parent_id: none
published_at: 2026-09-28T14:03Z
observed_at: 2026-10-01T09:15Z (export capture time)
capture_method: export
export_origin: account owner's data download, supplied by the user
inspected_part: video-interval
evidence_state: inaccessible
excerpt_or_observation: unknown
locator: whole video, length unknown
duplicate_group: none
duplicate_role: none
original_ref: none
duplicate_uncertain: no
access_gap: missing-field
exclusion: none
notes: The export lists a media file name, but the file wasn't included.
```

A comment on a live page, attributed to its commenter:

```yaml
id: E015
source_id: S005
platform: discussion forum
source_locator: https://forum.example.org/t/4410
discovered_via: E011
source_author: "@k_ramos"
parent_id: none
published_at: unknown
observed_at: 2026-10-14T16:40Z
capture_method: live-view
export_origin: not an export
inspected_part: comment
evidence_state: inspected
excerpt_or_observation: "Mine overheated twice on the first day."
locator: comment id 88213
duplicate_group: none
duplicate_role: none
original_ref: none
duplicate_uncertain: no
access_gap: none
exclusion: none
notes: A top-level comment in thread S005, which search card E011 led to. The page showed relative dates only, so the publication time is unknown.
```
