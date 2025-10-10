---
model: claude-sonnet-4-5-20250929
---

# Standup Notes Generator

Generate daily standup notes by reviewing Obsidian vault context and Jira tickets.

## Usage
```
/standup-notes
```

## Prerequisites

- Enable the **mcp-obsidian** provider with read/write access to the target vault.
- Configure the **atlassian** provider with Jira credentials that can query the team's backlog.
- Optional: connect calendar integrations if you want meetings to appear automatically.

## Process

1. **Gather Context from Obsidian**
   - Use `mcp__mcp-obsidian__obsidian_get_recent_changes` to find recently modified files
   - Use `mcp__mcp-obsidian__obsidian_get_recent_periodic_notes` to get recent daily notes
   - Look for project updates, completed tasks, and ongoing work

2. **Check Jira Tickets**
   - Use `mcp__atlassian__searchJiraIssuesUsingJql` to find tickets assigned to current user (fall back to asking the user for updates if the Atlassian connector is unavailable)
   - Filter for:
     - In Progress tickets (current work)
     - Recently resolved/closed tickets (yesterday's accomplishments)
     - Upcoming/todo tickets (today's planned work)

3. **Generate Standup Notes**
   Format:
   ```
   Morning!
   Yesterday:
   
   • [Completed tasks from Jira and Obsidian notes]
   • [Key accomplishments and milestones]
   
   Today:
   
   • [In-progress Jira tickets]
   • [Planned work from tickets and notes]
   • [Meetings from calendar/notes]
   
   Note: [Any blockers, dependencies, or important context]
   ```

4. **Write to Obsidian**
   - Create file in `Standup Notes/YYYY-MM-DD.md` format (or summarize in the chat if the Obsidian connector is disabled)
   - Use `mcp__mcp-obsidian__obsidian_append_content` to write the generated notes when available

## Implementation Steps

1. Get current user info from Atlassian
2. Search for recent Obsidian changes (last 2 days)
3. Query Jira for:
   - `assignee = currentUser() AND (status CHANGED FROM "In Progress" TO "Done" DURING (-1d, now()) OR resolutiondate >= -1d)`
   - `assignee = currentUser() AND status = "In Progress"`
   - `assignee = currentUser() AND status in ("To Do", "Open") AND (sprint in openSprints() OR priority in (High, Highest))`
4. Parse and categorize findings
5. Generate formatted standup notes
6. Save to Obsidian vault

## Context Extraction Patterns

- Look for keywords: "completed", "finished", "deployed", "released", "fixed", "implemented"
- Extract meeting notes and action items
- Identify blockers or dependencies mentioned
- Pull sprint goals and objectives