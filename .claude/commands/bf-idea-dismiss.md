# Dismiss Idea

Remove an idea from the active list without creating a GitHub issue.

## Arguments
- `$ARGUMENTS` - Required: idea ID (e.g., `3` or `3,5,7` for multiple)

## Instructions

1. **Load ideas:**
   ```bash
   cat .branch-flow/ideas/ideas.json
   ```

2. **Update the idea status:**
   ```json
   {
     "id": 3,
     "status": "dismissed",
     "dismissed_at": "2025-01-19T17:00:00Z",
     "dismiss_reason": null
   }
   ```

3. **Optionally ask for reason:**
   ```
   Dismissing idea #3: "Remove hardcoded Google Maps API key"
   
   Reason (optional, press Enter to skip):
   > Already tracked in existing issue #12
   ```

4. **Output:**
   ```
   ✅ Dismissed idea #3
   
   Title:  Remove hardcoded Google Maps API key from frontend code
   Reason: Already tracked in existing issue #12
   
   Dismissed ideas won't appear in /bf:ideas by default.
   Use /bf:ideas --status dismissed to see them.
   ```

## Dismissing Multiple Ideas

```bash
/bf:idea-dismiss 3,5,7
```

Output:
```
✅ Dismissed 3 ideas:
   #3 - Remove hardcoded Google Maps API key
   #5 - Implement route guards
   #7 - Sanitize HTML content

Use /bf:ideas --status dismissed to review dismissed ideas.
```

## Restoring Dismissed Ideas

If you change your mind:

```bash
/bf:idea-restore 3
```

This sets status back to "pending".

## Common Dismiss Reasons

- "Already tracked in issue #X"
- "Won't fix - by design"
- "Out of scope for this project"
- "Duplicate of idea #Y"
- "Fixed in recent commit"

## Bulk Dismiss by Category

To dismiss all ideas in a category:

```bash
/bf:idea-dismiss --category docs
```

Confirms before dismissing:
```
⚠️ This will dismiss 5 documentation ideas:
   #11 - Add troubleshooting section to README
   #12 - Document Vue component props with JSDoc
   #13 - Create contributor onboarding guide
   #14 - Add API documentation
   #15 - Document architecture with diagram

Proceed? [y/N]: 
```
