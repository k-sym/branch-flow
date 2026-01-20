# Start Implementation

Begin implementing the current task according to the plan.

## Instructions

1. Read current task from `.branch-flow/current-task.json`
   - If no plan exists, prompt to run `/bf:plan` first
   - If already building, resume from current task

2. Read configuration from `.branch-flow/config.json`

3. **Create Feature Branch** (if not already created):
   ```bash
   # Ensure we're on base branch and up to date
   git checkout [baseBranch]
   git pull origin [baseBranch]
   
   # Create feature branch
   git checkout -b [branchPrefix][spec-id]-[slug]
   ```
   
   Example: `bf/001-add-user-auth`

4. Update current-task.json with branch name

5. **Load Context:**
   - Read the spec file
   - Read the plan file
   - Read memory files
   - Note current task number

6. **Execute Current Task:**
   - Display the task details from plan
   - Work through the checklist items
   - Implement according to the detailed description
   - Follow patterns noted in the plan

7. **After Each Task:**
   - Run relevant tests if `requireTests` is true
   - Run linter if `requireLint` is true
   - If `autoCommit` is true, create meaningful commit:
     ```bash
     git add -A
     git commit -m "[spec-id] Task [n]: [task name]"
     ```

8. **Task Completion:**
   - Verify the task's completion criteria
   - Update current-task.json to next task
   - If more tasks remain, continue to next
   - If all tasks complete, update status to "review-ready"

9. Output during build:
```
🔨 Building: 001-[name]

🌿 Branch: bf/001-[slug]

📋 Task 2 of 5: Write authentication tests

📝 Description:
   [task description from plan]

✅ Checklist:
   - [ ] Test case 1
   - [ ] Test case 2
   - [ ] Run tests and verify passing

Working on this task...
```

10. After completing a task:
```
✅ Task 2 Complete: Write authentication tests

📝 Changes:
   - Created: src/auth/auth.test.ts
   - Modified: package.json

💾 Committed: [commit hash]
   "[spec-id] Task 2: Write authentication tests"

📋 Progress: 2/5 tasks complete

Next task: Task 3 - Implement JWT token generation
Continue? (y/n) or run /bf:review to check progress
```

## Resuming Work

If you return to a partially completed build:

```
🔨 Resuming: 001-[name]

🌿 Branch: bf/001-[slug]
📋 Progress: 2/5 tasks complete

Last completed: Task 2 - Write authentication tests
Next task: Task 3 - Implement JWT token generation

Continue from Task 3?
```

## Build Principles

- **Follow the plan**: Don't deviate without updating spec
- **One task at a time**: Complete each task before moving on
- **Commit frequently**: Each task = one commit
- **Test as you go**: Don't accumulate untested code
- **Stay focused**: Avoid scope creep during build
