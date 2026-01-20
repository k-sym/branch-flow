# Documentation Research Skill

**Trigger:** When implementation requires external library/framework documentation

**Purpose:** Fetch, extract, and summarize documentation efficiently to minimize context usage while maintaining accuracy.

## When This Skill Applies

- Planning phase identifies external dependencies
- Implementation encounters unfamiliar API
- Need to verify correct usage patterns
- Checking for breaking changes or deprecations

## Core Principle: Extract, Don't Embed

❌ **Don't:** Load full documentation into context
✅ **Do:** Extract relevant snippets into structured summaries

## Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Identify Need  │────▶│  Fetch via MCP  │────▶│ Extract & Save  │
│                 │     │  (Context7)     │     │  (~50 lines)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                        ┌───────────────────────────────┘
                        ▼
                ┌─────────────────┐
                │ Reference File  │
                │ .branch-flow/   │
                │ docs/lib-ref.md │
                └─────────────────┘
```

## Extraction Template

When fetching documentation, extract into this structure:

```markdown
# [Library] Quick Reference

**Fetched:** YYYY-MM-DD
**Version:** x.y.z (if known)
**Task:** [current spec ID if applicable]

## Installation
```bash
npm install [package]
```

## Key APIs

### [API Name]
```typescript
// Signature only - no lengthy explanations
function apiName(param: Type): ReturnType
```
**Use for:** [one line purpose]
**Example:**
```typescript
// Minimal working example - 3-5 lines max
```

## Patterns for This Task

### [Pattern relevant to current work]
```typescript
// Just the pattern, no boilerplate
```

## Gotchas
- [ ] [Caveat that could cause bugs]
- [ ] [Common mistake to avoid]
- [ ] [Version-specific behavior]

## Links
- Docs: [URL]
```

## Size Guidelines

| Section | Target Size |
|---------|-------------|
| Total file | 50-100 lines |
| Per API | 5-10 lines |
| Examples | 3-5 lines each |
| Gotchas | 1 line each |

## MCP Integration

### Context7 Setup

Ensure Context7 MCP is configured in Claude Code:

**Option 1: claude_desktop_config.json**
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp"]
    }
  }
}
```

**Option 2: .claude/mcp.json (project-level)**
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp"]
    }
  }
}
```

### Using Context7

```
# Search for library docs
context7_search("react-query useQuery")

# Get specific documentation
context7_get_docs("@tanstack/react-query", "useQuery")
```

## During Planning Phase

When `/bf:plan` identifies external dependencies:

1. **Detect dependencies** from:
   - package.json / requirements.txt / Cargo.toml
   - Import statements in related files
   - Spec requirements mentioning libraries

2. **Prompt for doc fetch:**
   ```
   📚 This task involves:
      - react-query (queries)
      - zod (validation)
   
   Fetch latest docs? (y/n/select)
   ```

3. **If yes**, for each library:
   - Fetch via Context7
   - Extract relevant APIs only
   - Save to `.branch-flow/docs/`
   - Add reference to plan

4. **Add to plan:**
   ```markdown
   ## Documentation References
   
   | Library | Reference | Key APIs |
   |---------|-----------|----------|
   | react-query | docs/react-query-ref.md | useQuery, useMutation |
   | zod | docs/zod-ref.md | z.object, z.string |
   ```

## During Build Phase

When implementing and need to check documentation:

1. **Check existing reference first:**
   ```bash
   ls .branch-flow/docs/
   ```

2. **If reference exists and recent** (< 7 days):
   - Read the concise reference
   - Use patterns directly

3. **If missing or stale:**
   - Run `/bf:docs [library]`
   - Continue implementation

4. **If reference insufficient:**
   - Fetch specific API via Context7
   - Append to existing reference
   - Don't replace entire file

## Context Efficiency

### Before (Full Docs)
```
Context usage: ~15,000 tokens for react-query docs
Relevance: ~10% actually needed for task
```

### After (This Skill)
```
Context usage: ~500 tokens for reference file
Relevance: ~90% directly applicable
```

### Refresh Strategy

| Situation | Action |
|-----------|--------|
| New library | Create reference |
| Existing + recent | Use as-is |
| Existing + stale | Update relevant sections |
| Need more detail | Append, don't replace |

## File Organization

```
.branch-flow/
└── docs/
    ├── react-query-ref.md
    ├── prisma-ref.md
    ├── nextjs-app-router-ref.md
    └── zod-ref.md
```

## Cleanup

After task completion, optionally archive docs:
- Keep if library will be used again
- Delete if one-off dependency
- Note in learnings if patterns were useful
