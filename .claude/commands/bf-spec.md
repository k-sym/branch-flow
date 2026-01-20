# Create Task Specification

Create a new task specification for Branch Flow.

## Arguments
- `$ARGUMENTS` - Brief description of what to build (optional, will prompt if not provided)

## Instructions

1. If no task description provided, ask:
   - "What would you like to build? Describe the feature or fix."

2. Read `.branch-flow/config.json` to get `nextSpecId`

3. Generate a slug from the description (lowercase, hyphens, max 50 chars)

4. **Brainstorm Phase** - Before writing the spec, have a conversation:
   - What problem does this solve?
   - Who is the user/audience?
   - What are the success criteria?
   - Are there any constraints or dependencies?
   - What's out of scope?

5. Create specification file `.branch-flow/specs/[id]-[slug].md`:

```markdown
# Spec [ID]: [Title]

**Created:** [date]
**Status:** draft | ready | in-progress | completed | abandoned
**Branch:** (will be filled during build)

## Summary
[One paragraph description of what this task accomplishes]

## Problem Statement
[What problem does this solve? Why is it needed?]

## Requirements

### Must Have
- [ ] Requirement 1
- [ ] Requirement 2

### Should Have
- [ ] Nice-to-have 1

### Out of Scope
- Thing explicitly not included

## Acceptance Criteria
When this task is complete:
1. [Testable criterion 1]
2. [Testable criterion 2]
3. [Testable criterion 3]

## Technical Notes
[Any technical considerations, constraints, or approaches to consider]

## Dependencies
- [Other specs, external services, etc.]

## References
- [Links to relevant docs, issues, discussions]

---
*Spec created by Branch Flow*
```

6. Update `nextSpecId` in config.json

7. Save current task reference:
```json
// .branch-flow/current-task.json
{
  "specId": "001",
  "specFile": "001-feature-name.md",
  "status": "spec-created",
  "createdAt": "2025-01-18T...",
  "branch": null
}
```

8. Output:
```
📋 Spec Created: 001-[slug]

📄 File: .branch-flow/specs/001-[slug].md

📝 Summary:
   [brief summary]

✅ Requirements: [count] must-have, [count] should-have
🎯 Acceptance Criteria: [count] items

Next: Review the spec, then run /bf:plan to create implementation plan
```

## Tips for Good Specs

- Be specific about acceptance criteria
- Include examples where helpful
- Note what's explicitly out of scope
- Link to relevant context (issues, docs, designs)
- Keep specs focused - one feature per spec
