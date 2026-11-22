# Renders a short clip of the Verified judge catching a skipped test.
# No camera, no voice: VHS types the commands and records the terminal.
# Render locally with `vhs tools/verified/tapes/gate-catches-skipped-test.tape`,
# or run the "Verified clips" workflow by hand from the Actions tab.

Output tools/verified/tapes/out/gate-catches-skipped-test.gif

Require uv
Require git

Set Shell "bash"
Set FontSize 16
Set Width 1200
Set Height 640
Set TypingSpeed 40ms

Type "# An agent 'fixes' a failing test by skipping it. The judge fails the run."
Enter
Sleep 1s
Type "uv run --project plugins/plugin-eval --extra dev pytest -q tools/tests/test_verified.py -k 'skipping_a_test or reference_solution_passes' -v"
Enter
Wait+Screen@120s /passed/
Sleep 4s
