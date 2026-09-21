# Creative and tracking — draw for the eye, tag every outbound link

How to build the creative that carries the message, and how to keep the data that decides whether the channel lives or dies.

## Graphics: Draw for the Eye

The human eye sees sharply only in a small focal spot (the fovea), aimed at the center. Everything else is background that the brain paints in. Use that.

- **Always have a background and a scene.** The eye needs context around the subject.
- **Always have a hero.** One main subject inside the scene. It can sit anywhere in the frame — center is not required — but it must be there, with the scene built around it.
- **Movement is the most important and the hardest.** The eye locks onto motion before anything else, so a banner or a creative must carry movement — even in a single still frame. Portraying that motion correctly is exactly the job of the image and video models.

The eye is trained on reality, but our task is to transform reality into the format of a picture or a video. Everything that happens in real life must be present in the image — accent, background, scene, movement. Draw it so the viewer's mind can reconstruct and understand it without effort.

## Tagging: Every Outbound Link Carries UTM

A campaign you cannot attribute is a campaign you cannot kill. The rule is mechanical:
**every link that leaves for your own property carries UTM; internal links never do.**

- `utm_source` — the channel that sent the click: `devto`, `github`, `npm`, `telegram`, `habr`, `reddit`, `colony`.
- `utm_medium` — the placement: `article`, `readme`, `package`, `post`, `comment`, `profile`, `bio`.
- `utm_campaign` — the product or cluster: `mindset`, `tapac`, `hire`, `lyzhi`, `engine`.

Rules that keep the data clean:

- Tag only destinations you own. A third-party link stays clean.
- **Never tag internal site links.** An internal link with UTM restarts the session, so one visit looks like two and the page's own report becomes wrong.
- Never tag twice: a URL that already has `utm_source` is done. Tagging happens before the text ships, not after.
- Keep existing query params — append, never rebuild the URL.
- Apply the tags in one pass at publish time, by hand: append `utm_source`, `utm_medium`, and `utm_campaign` to the destination URL before the text goes out.

Why it pays: a channel with a tagged link can be read in the same report as everything else and killed on evidence. An untagged one only feels like it is working.
