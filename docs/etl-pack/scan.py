import re, pathlib, json, collections
groups = {
 "confluence": r"confluence|atlassian|wiki",
 "html_md": r"markdown|xhtml|html\s*(?:to|->)\s*markdown|beautifulsoup|bs4|lxml|markdownify|pandoc|html2text|scrap(?:e|ing|er)|crawl(?:er|ing)?",
 "knowledge": r"knowledge\s+(?:base|module|graph)s?|rag|retrieval|embeddings?|chunk(?:ing|s)?|vector\s+(?:store|database|db)",
 "docs": r"documentation|docs[- ]as[- ]code|mkdocs|docusaurus|sphinx|frontmatter|front[- ]matter|technical\s+writ(?:ing|er)|information\s+architecture",
 "agentctx": r"progressive\s+disclosure|SKILL\.md|AGENTS\.md|CLAUDE\.md|llms\.txt|context\s+(?:file|window|engineering)",
 "api": r"pagination|paginat(?:e|ed)|rate[- ]limit(?:s|ing)?|retry-after|cursor|httpx|incremental|checkpoint(?:s|ing)?|idempoten(?:t|cy)",
 "quality": r"link\s+(?:check|integrity|rot)|dead\s+links?|broken\s+links?|markdownlint|golden\s+files?|snapshot\s+tests?",
 "safety": r"pii|redact(?:ion|ed)?|secrets?\s+(?:scan|detect)|data\s+classification",
}
rx = {k: re.compile(r"\b(?:%s)\b" % v, re.I) for k, v in groups.items()}
rows = []
for f in sorted(pathlib.Path("plugins").glob("*/**/*.md")):
    parts = f.parts
    plugin = parts[1]
    if len(parts) < 4 or parts[2] not in ("agents", "commands", "skills"):
        continue
    asset = "/".join(parts[2:4]) if parts[2] == "skills" else "/".join(parts[2:])
    text = f.read_text(errors="ignore")
    hits = {}
    for k, r in rx.items():
        lines = [i+1 for i, l in enumerate(text.splitlines()) if r.search(l)]
        if lines:
            first = text.splitlines()[lines[0]-1].strip()[:110]
            hits[k] = (len(lines), f"{f}:{lines[0]}", first)
    if hits:
        rows.append((plugin, asset, str(f), hits))
# aggregate per asset
agg = collections.defaultdict(lambda: collections.Counter())
ex = collections.defaultdict(dict)
for plugin, asset, f, hits in rows:
    for k, (n, loc, first) in hits.items():
        agg[(plugin, asset)][k] += n
        ex[(plugin, asset)].setdefault(k, (loc, first))
json.dump({f"{p}|{a}": {"counts": dict(c), "examples": ex[(p,a)]} for (p,a), c in agg.items()},
          open("/tmp/claude-0/-home-user/59c1c3ba-1f22-5d42-85d5-c5fde6d40b01/scratchpad/pack/scan.json","w"), indent=1)
# score: groups weighted toward this project
w = {"confluence":5,"html_md":3,"knowledge":3,"docs":2,"agentctx":3,"api":1,"quality":3,"safety":2}
scored = sorted(((sum(w[k]*min(v,10) for k,v in c.items()), p, a, dict(c)) for (p,a),c in agg.items()), reverse=True)
for s,p,a,c in scored[:70]:
    print(f"{s:4} {p}/{a}  {c}")
print(len(agg), "assets with any hit")
