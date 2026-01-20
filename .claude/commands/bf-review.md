# QA Review Loop

Run quality assurance validation on the current build.

## Instructions

1. Read current task from `.branch-flow/current-task.json`
   - Verify we're in a build state
   - Load spec and plan for reference

2. **Automated Checks:**

   Run each check and collect results:
   
   ```bash
   # Tests
   npm test / pytest / cargo test / etc.
   
   # Linting
   npm run lint / ruff check / cargo clippy / etc.
   
   # Type checking (if applicable)
   npm run typecheck / mypy / etc.
   
   # Build verification
   npm run build / cargo build / etc.
   ```

3. **Spec Compliance Check:**
   
   Go through each acceptance criterion from the spec:
   - Is it implemented?
   - Is it testable/tested?
   - Does it work as specified?

4. **Code Quality Review:**
   
   Review the diff against base branch:
   ```bash
   git diff [baseBranch]..HEAD
   ```
   
   Check for:
   - Code follows project conventions
   - No debugging code left behind
   - Error handling is appropriate
   - Edge cases are handled
   - Documentation updated where needed

5. **Generate Review Report:**

```markdown
# QA Review: [Spec ID] - [Name]

**Date:** [timestamp]
**Branch:** bf/[id]-[slug]
**Commits:** [count]

## Automated Checks

| Check | Status | Details |
|-------|--------|---------|
| Tests | ✅ PASS | 42 passed, 0 failed |
| Lint | ⚠️ WARN | 2 warnings |
| Types | ✅ PASS | No errors |
| Build | ✅ PASS | Built successfully |

## Spec Compliance

| Requirement | Status | Notes |
|-------------|--------|-------|
| [Req 1] | ✅ | Implemented and tested |
| [Req 2] | ✅ | Implemented and tested |
| [Req 3] | ❌ | Missing error handling |

## Acceptance Criteria

- [x] Criterion 1 - Verified
- [x] Criterion 2 - Verified  
- [ ] Criterion 3 - **NEEDS WORK**

## Code Quality

### Strengths
- Well-structured code
- Good test coverage

### Issues Found
1. **[HIGH]** Missing error handling in auth.ts:45
2. **[MEDIUM]** Could add input validation
3. **[LOW]** Consider extracting helper function

## Files Changed
- `src/auth/auth.ts` (+120, -15)
- `src/auth/auth.test.ts` (+89, -0)
- `package.json` (+2, -0)

## Recommendation

[ ] ✅ READY TO MERGE
[x] 🔧 NEEDS FIXES (see issues above)
[ ] ❌ MAJOR ISSUES
```

6. **QA Loop:**
   
   If issues found:
   - Present the issues clearly
   - Ask to fix the issues
   - After fixes, re-run `/bf:review`
   
   Continue loop until:
   - All automated checks pass
   - All acceptance criteria met
   - No HIGH severity issues remain

7. Update current-task.json:
```json
{
  ...
  "status": "review-passed" | "needs-fixes",
  "reviewedAt": "...",
  "reviewAttempts": 2,
  "lastReview": {
    "tests": "pass",
    "lint": "pass",
    "specCompliance": 100,
    "issues": []
  }
}
```

8. Output:
```
🔍 QA Review: 001-[name]

📊 Automated Checks:
   ✅ Tests: 42 passed
   ✅ Lint: Clean
   ✅ Types: No errors
   ✅ Build: Success

📋 Spec Compliance: 100%
   ✅ All 5 acceptance criteria met

🔎 Code Quality:
   ✅ No high-severity issues
   ⚠️ 1 medium suggestion (optional)

✅ READY TO MERGE

Run /bf:merge to complete this task
```

Or if issues:
```
🔍 QA Review: 001-[name]

📊 Automated Checks:
   ✅ Tests: 40 passed, 2 failed
   ⚠️ Lint: 3 warnings
   
📋 Spec Compliance: 80%
   ❌ Missing: Error handling for invalid tokens

🔎 Issues Found:
   1. [HIGH] Test failure in auth.test.ts:45
   2. [HIGH] Missing requirement: token expiry
   3. [MEDIUM] Lint warning: unused import

🔧 NEEDS FIXES

Fix the issues above, then run /bf:review again
```
