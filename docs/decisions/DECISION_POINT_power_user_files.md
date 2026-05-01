# Decision Point: Per-Plugin GEMINI.md Files

**Date:** 2026-05-01  
**Finding:** Power user benefit claim in ADR 2 was invalid. The 79 per-plugin GEMINI.md files provide NO automatic context loading with current Gemini CLI.

---

## The Issue

You currently have:
```
plugins/security-scanning/GEMINI.md
plugins/backend-development/GEMINI.md
... 77 more files
```

But Gemini CLI looks for:
```
plugins/security-scanning/.gemini/GEMINI.md
plugins/backend-development/.gemini/GEMINI.md
```

**Result:** Files are never auto-loaded.

---

## Three Options

### Option A: Keep Files As-Is (Current ADR 2 Choice)

**Justification:**
- Files serve as human-readable documentation in the repo
- Hedge bet on future Gemini CLI features (extension-relative `@{path}`)

**Pros:**
- Minimal change
- Ready for future features when they arrive

**Cons:**
- 142 KB of currently unused files
- Misleading Option 3 description (now corrected in audit)
- Power users don't get the promised benefit

**When to choose:** If you believe Gemini CLI will add extension-relative path resolution in the near term.

---

### Option B: Move Files to `.gemini/` Subdirectories

```
plugins/security-scanning/.gemini/GEMINI.md
plugins/backend-development/.gemini/GEMINI.md
... 77 more files
```

**Justification:**
- Makes Option 3 claim ACTUALLY TRUE
- Power users get immediate benefit when they `cd plugins/<name>/`

**Pros:**
- Matches Gemini CLI's actual file resolution
- Power users get scoped context automatically
- Fulfills the original vision

**Cons:**
- Reorganize 79 plugin directories
- Update generator scripts
- Still no benefit for normal extension users

**Effort:** Medium (script-driven reorganization)

**When to choose:** If you want the power user benefit to work immediately.

---

### Option C: Remove Files Entirely

```
plugins/  (only agents/, commands/, skills/ directories)
```

**Justification:**
- Keep implementation clean
- Only use root GEMINI.md for all users
- Avoid dead weight

**Pros:**
- Simpler codebase
- No hedge bet needed
- Clear incentive structure (install extension to get all context)

**Cons:**
- Lose documentation that developers find in the repo
- Can't leverage future extension-relative features
- Less explorability for power users

**When to choose:** If you want a clean, minimal implementation and don't expect extension-relative features soon.

---

## Recommendation

**Option B (Move to `.gemini/`)** if:
- You want the power user promise to be real
- You're committed to developer experience
- The reorganization is acceptable

**Option A (Keep as-is)** if:
- You're confident Gemini CLI will add extension-relative paths
- You want to avoid reorganization now
- The documentation value for repo browsers is enough

**Option C (Remove)** if:
- You prefer minimal, clean design
- The root GEMINI.md is sufficient
- Power user benefits are lower priority

---

## Next Steps

1. **Choose an option** based on your priorities
2. **If Option A:** Consider adding explicit future-proofing note to ADR 2
3. **If Option B:** Use update script to reorganize 79 plugin directories
4. **If Option C:** Remove generator script for per-plugin files

