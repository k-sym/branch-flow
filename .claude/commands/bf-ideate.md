# Generate Ideas from Codebase Analysis

Analyze the codebase and generate categorized improvement ideas.

## Arguments
- `$ARGUMENTS` - Optional: `--refresh` to regenerate, `--category <cat>` to focus on one category

## Categories

Ideas are generated across 5 categories:

| Category | Icon | Focus Areas |
|----------|------|-------------|
| **Code Quality** | `</>` | Duplication, complexity, refactoring, testing, linting |
| **UI/UX** | `✨` | Usability, accessibility, interactions, visual consistency |
| **Security** | `🔒` | Vulnerabilities, auth, data exposure, input validation |
| **Documentation** | `📚` | Missing docs, API docs, architecture, onboarding |
| **Performance** | `⚡` | Slow operations, caching, bundle size, memory |

## Instructions

1. **Check for existing ideas:**
   ```bash
   ls .branch-flow/ideas/
   ```
   
   If ideas exist and `--refresh` not passed, inform user:
   ```
   💡 Found 25 existing ideas. Use /bf:ideas to review them.
      Run /bf:ideate --refresh to regenerate.
   ```

2. **Load project context:**
   - Read `.branch-flow/memory/project-context.md`
   - Read `.branch-flow/config.json` for project type hints
   - Check for package.json, requirements.txt, etc. for tech stack

3. **Analyze codebase systematically:**

   For each category, examine relevant aspects:

   **Code Quality:**
   - Look for large files (500+ lines)
   - Find duplicated patterns across files
   - Check for missing tests
   - Look for TODO/FIXME comments
   - Check for linting/formatting config
   - Identify complex functions (high cyclomatic complexity)

   **UI/UX:**
   - Check for accessibility attributes (aria-*, role)
   - Look for hardcoded strings (i18n opportunities)
   - Find inconsistent error handling/messages
   - Check for loading states, empty states
   - Look for form validation patterns

   **Security:**
   - Search for hardcoded secrets/API keys
   - Check for console.log with sensitive data
   - Look for SQL/NoSQL injection risks
   - Check authentication/authorization patterns
   - Find unvalidated user input
   - Check dependency vulnerabilities (if package-lock exists)

   **Documentation:**
   - Check for missing README sections
   - Look for undocumented public APIs
   - Find complex code without comments
   - Check for missing CONTRIBUTING guide
   - Look for outdated documentation

   **Performance:**
   - Find N+1 query patterns
   - Look for missing pagination
   - Check for unbounded loops/iterations
   - Find missing caching opportunities
   - Look for large bundle imports

4. **Generate 5 ideas per category** (25 total, like Auto-Claude)

   For each idea, determine:
   - **Title**: Clear, actionable (e.g., "Split monolithic audit store into smaller domain stores")
   - **Description**: Specific details with file names, line numbers where possible
   - **Priority**: `high`, `medium`, `low` (or `major`, `minor` for code quality)
   - **Effort estimate**: `small`, `medium`, `large`

5. **Save ideas to `.branch-flow/ideas/ideas.json`:**

```json
{
  "generated_at": "2025-01-19T16:45:00Z",
  "project": "project-name",
  "total": 25,
  "ideas": [
    {
      "id": 1,
      "category": "security",
      "priority": "high",
      "effort": "small",
      "title": "Remove hardcoded Google Maps API key from frontend code",
      "description": "The Google Maps API key 'AIzaSy...' is hardcoded directly in the frontend component AuditDetail.vue (line 172). This key is exposed in the client-side code and can be extracted by anyone viewing the source.",
      "files": ["src/components/AuditDetail.vue"],
      "lines": [172],
      "status": "pending",
      "github_issue": null
    },
    {
      "id": 2,
      "category": "code",
      "priority": "major",
      "effort": "large",
      "title": "Split FindingModal.vue component into smaller focused components",
      "description": "FindingModal.vue is 907 lines - nearly double the recommended maximum for a Vue component. It handles: dialog state, form management, image capture, image compression, image annotation integration, storage health checks, validation, and submission.",
      "files": ["src/components/FindingModal.vue"],
      "lines": null,
      "status": "pending",
      "github_issue": null
    }
  ]
}
```

6. **Output summary:**

```
💡 Ideation Complete!

Generated 25 improvement ideas:

   </> Code Quality     5 ideas (2 major, 3 minor)
   ✨  UI/UX            5 ideas (1 high, 3 medium, 1 low)
   🔒 Security          5 ideas (2 high, 3 medium)
   📚 Documentation     5 ideas (1 high, 2 medium, 2 low)
   ⚡ Performance       5 ideas (1 high, 2 medium, 2 low)

Top Priority:
   🔒 [HIGH] Remove hardcoded Google Maps API key from frontend code
   🔒 [HIGH] Implement route guards for authenticated routes
   </> [MAJOR] Extract duplicated image capture logic into a composable

Use /bf:ideas to browse all ideas
Use /bf:idea-approve <id> to create a GitHub issue
```

## Focusing on One Category

```bash
/bf:ideate --category security
```

This will only analyze and generate security-related ideas.

## Tips for Better Ideas

The quality of ideas depends on thorough analysis. When examining code:

1. **Be specific** - Include file names, line numbers, function names
2. **Explain impact** - Why does this matter?
3. **Suggest solution** - Brief hint at how to fix
4. **Consider effort** - Is this a quick fix or major refactor?

## Integration with Workflow

Ideas flow into the standard Branch Flow workflow:

```
/bf:ideate           → Generate ideas
/bf:ideas            → Review and filter
/bf:idea-approve 3   → Create GitHub issue #45
/bf:spec "Fix #45"   → Create spec linked to issue
/bf:build            → Branch: bf/003-fix-45-route-guards
```
