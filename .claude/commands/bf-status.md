# Show Task Status

Display the current state of Branch Flow.

## Instructions

1. Read `.branch-flow/current-task.json`

2. If no active task:
```
📊 Branch Flow Status

🔹 Status: Idle - No active task

📁 Project: [project name]
🌿 Base branch: main

📋 Completed specs: [count]
📝 Draft specs: [count]

Run /bf:spec to start a new task
```

3. If active task exists, show detailed status:

```
📊 Branch Flow Status

📋 Active Task: 001-[name]
🔹 Status: [status]
🌿 Branch: bf/001-[slug]

## Progress

Phase: [current phase]
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  ✅ SPEC    │─│  ✅ PLAN    │─│  🔨 BUILD   │─│  ○ REVIEW   │─│  ○ MERGE    │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘

## Build Progress
[████████░░░░░░░░░░░░] 40% (2/5 tasks)

Completed:
  ✅ Task 1: Setup authentication module
  ✅ Task 2: Write authentication tests

Current:
  🔨 Task 3: Implement JWT token generation

Remaining:
  ○ Task 4: Add token refresh logic
  ○ Task 5: Integration testing

## Timeline
Created:   2025-01-18 10:30 AM
Planned:   2025-01-18 10:45 AM
Started:   2025-01-18 11:00 AM
Duration:  2h 15m

## Files Changed (this session)
- src/auth/auth.ts
- src/auth/auth.test.ts
- package.json

## Quick Actions
- /bf:build    Continue implementation
- /bf:review   Run QA check
- /bf:abort    Abandon task
```

4. Status values:
   - `spec-created` - Spec written, needs planning
   - `planned` - Plan created, ready to build
   - `building` - Implementation in progress
   - `review-ready` - Build complete, needs QA
   - `needs-fixes` - QA found issues
   - `review-passed` - QA passed, ready to merge
   - `completed` - Successfully merged
   - `abandoned` - Task was aborted

5. Also show recent history:
```
## Recent Activity

| Spec | Status | Completed |
|------|--------|-----------|
| 001-add-user-auth | ✅ completed | 2025-01-17 |
| 002-fix-login-bug | ✅ completed | 2025-01-16 |
```
