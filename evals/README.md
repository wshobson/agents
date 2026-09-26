# Evals

This directory holds evaluation data for the skills in this repository.

## Static score snapshot

`static-score-snapshot.json` records how the plugin-eval static layer scores every skill at quick depth. Each entry holds the static score, the sub-scores, the composite score, the badge, and a sha256 digest of the skill's files.

`make test` runs two tests from `tools/tests/test_static_score_snapshot.py` against it.

- The first test scores every skill again and compares the numbers with the snapshot. It fails when a skill's files did not change but its numbers did, which means the scoring code changed. The failure lists each skill whose numbers moved.
- The second test checks that the snapshot is fresh. It fails when fewer than half of the entries still match the skills in the repository.

The snapshot is keyed by a hash of each skill's content. When you edit a skill, its digest changes and the tests skip it, so editing a skill never fails the first test. When a skill links to other skills, its digest also covers the names of the skill directories next to it, so adding a skill does not fail the test either.

Run `make eval-snapshot` and commit the updated file in either of these cases:

- You changed the scoring code on purpose, and the first test lists the skills whose numbers moved.
- The second test fails because fewer than half of the entries match. A pull request that edits many skills at once, such as a sweep across the whole repository, can cause this.

## Trace-based evals

The LLM judge and Monte Carlo layers of plugin-eval are experimental. They have not been checked against human labels.

A trace-based eval program is in progress. It follows the method that Hamel Husain and Shreya Shankar teach, which starts with error analysis. People read traces of real Claude Code sessions that use these skills and write down what went wrong. Checks are then written for the failures they find, and an LLM judge is trusted only after it has been checked against human labels.
