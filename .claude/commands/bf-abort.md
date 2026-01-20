# Abort Current Task

Abandon the current task and clean up.

## Instructions

1. Read `.branch-flow/current-task.json`
   - If no active task, inform user and exit

2. **Confirm Abort:**
```
⚠️ Abort Task: 001-[name]

This will:
- Discard uncommitted changes
- Delete the feature branch
- Mark the spec as abandoned

Current progress: 2/5 tasks complete
Uncommitted changes: 3 files

Are you sure? (y/n)
```

3. **If confirmed:**

   a. Stash any uncommitted work (just in case):
   ```bash
   git stash push -m "branch-flow-abort-001-[slug]"
   ```

   b. Switch to base branch:
   ```bash
   git checkout [baseBranch]
   ```

   c. Delete feature branch:
   ```bash
   git branch -D bf/[spec-id]-[slug]
   ```

4. **Update spec status:**
   ```markdown
   **Status:** abandoned
   **Abandoned:** [date]
   **Reason:** [ask user for optional reason]
   **Progress:** 2/5 tasks completed
   ```

5. **Clear current task:**
   ```json
   {
     "specId": null,
     "status": "idle",
     "lastAbandoned": {
       "specId": "001",
       "specFile": "001-feature-name.md",
       "abandonedAt": "...",
       "progress": "2/5"
     }
   }
   ```

6. **Optional: Add to learnings:**
   ```markdown
   ## [Date] - Abandoned: [Spec Title]
   
   ### Why Abandoned
   - [User's reason if provided]
   
   ### Lessons
   - [What can be learned from this]
   ```

7. Output:
```
🛑 Task Abandoned: 001-[name]

🧹 Cleanup:
   ✅ Switched to main
   ✅ Deleted branch bf/001-[slug]
   ✅ Spec marked as abandoned
   💾 Changes stashed: branch-flow-abort-001-[slug]

📝 Note: Your work is saved in git stash if needed later.
   To recover: git stash list
   
Ready for next task. Run /bf:spec to start fresh.
```

## Recovery Option

If user wants to resume an abandoned task:
```bash
# Find the stash
git stash list

# Create new branch and apply
git checkout -b bf/001-[slug]-v2
git stash apply stash@{0}
```

Then manually update current-task.json to resume.
