# Messaging Pattern Templates

Ready-to-use message templates for common team communication scenarios.

## Task Assignment

```
You've been assigned task #{id}: {subject}.

Owned files:
- {file1}
- {file2}

Key requirements:
- {requirement1}
- {requirement2}

Interface contract:
- Import {types} from {shared-file}
- Export {types} for {other-teammate}

Let me know if you have questions or blockers.
```

## Integration Point Notification

```
My side of the {interface-name} interface is complete.

Exported from {file}:
- {function/type 1}
- {function/type 2}

You can now import these in your owned files. The contract matches what we agreed on.
```

## Blocker Report

```
I'm blocked on task #{id}: {subject}.

Blocker: {description of what's preventing progress}
Impact: {what can't be completed until this is resolved}

Options:
1. {option 1}
2. {option 2}

Waiting for your guidance.
```

## Task Completion Report

```
Task #{id} complete: {subject}

Changes made:
- {file1}: {what changed}
- {file2}: {what changed}

Integration notes:
- {any interface changes or considerations for other teammates}

Ready for next assignment.
```

## Review Finding Summary

```
Review complete for {target} ({dimension} dimension).

Summary:
- Critical: {count}
- High: {count}
- Medium: {count}
- Low: {count}

Top finding: {brief description of most important finding}

Full findings attached to task #{id}.
```

## Investigation Report Summary

```
Investigation complete for hypothesis: {hypothesis summary}

Verdict: {Confirmed | Falsified | Inconclusive}
Confidence: {High | Medium | Low}

Key evidence:
- {file:line}: {what was found}
- {file:line}: {what was found}

{If confirmed}: Recommended fix: {brief fix description}
{If falsified}: Contradicting evidence: {brief description}

Full report attached to task #{id}.
```

## Shutdown Acknowledgment

When you receive a shutdown request, respond with the shutdown_response tool. But you may also want to send a final status message:

```
Wrapping up. Current status:
- Task #{id}: {completed/in-progress}
- Files modified: {list}
- Pending work: {none or description}

Ready for shutdown.
```
