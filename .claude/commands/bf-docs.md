# Fetch Documentation

Fetch and summarize documentation for libraries/frameworks using Context7 MCP.

## Arguments
- `$ARGUMENTS` - Library or component name (e.g., "react-query", "prisma", "nextjs app router")

## Prerequisites

Context7 MCP must be configured. Add to your Claude Code MCP settings:

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

## Instructions

1. Parse the library/component name from arguments

2. Use Context7 MCP to fetch documentation:
   ```
   Use the context7 MCP to search for documentation on: $ARGUMENTS
   ```

3. **Extract and Summarize** - Don't keep full docs in context. Instead, extract:
   - Key API signatures
   - Common patterns/examples
   - Gotchas and best practices
   - Version-specific notes if relevant

4. Create a concise reference file `.branch-flow/docs/[library]-ref.md`:

```markdown
# [Library] Quick Reference

**Fetched:** [date]
**Version:** [if known]
**Source:** Context7

## Key APIs

### [Function/Component 1]
```typescript
signature here
```
- Purpose: [one line]
- Returns: [type]
- Common params: [list key ones]

### [Function/Component 2]
...

## Patterns

### [Pattern Name]
```typescript
// Concise example - just the essential pattern
```

## Gotchas
- [Important caveat 1]
- [Important caveat 2]

## See Also
- [Link to full docs if needed]
```

5. If there's an active task, also append to the plan:
   ```markdown
   ## Documentation References
   - [Library]: See `.branch-flow/docs/[library]-ref.md`
   ```

6. Output:
```
📚 Documentation: react-query

✅ Fetched and summarized to:
   .branch-flow/docs/react-query-ref.md

📋 Key APIs extracted:
   - useQuery
   - useMutation
   - useQueryClient
   - QueryClientProvider

📝 Patterns documented:
   - Basic query
   - Mutation with optimistic update
   - Infinite queries
   - Prefetching

⚠️ Gotchas noted: 3

Context saved (~45 lines). Full docs available via Context7.
```

## Usage Examples

```bash
# During planning
/bf:docs prisma

# Multiple lookups
/bf:docs "nextjs server actions"
/bf:docs "zod validation"

# Specific feature
/bf:docs "tanstack table column filtering"
```

## Integration with Workflow

### During /bf:plan
When creating an implementation plan, if external libraries are involved:
1. Prompt: "This task uses [library]. Fetch docs? (y/n)"
2. If yes, run `/bf:docs [library]`
3. Reference in plan under "Documentation References"

### During /bf:build
When implementing and need to check an API:
1. First check if `.branch-flow/docs/[library]-ref.md` exists
2. If not or need more detail, run `/bf:docs [library]`
3. Consult the concise reference, not full docs

## Why This Approach?

| Approach | Context Cost | Freshness |
|----------|--------------|-----------|
| Full docs in context | 🔴 High (10k+ tokens) | ✅ Current |
| Pre-written notes | 🟢 Low | 🔴 May be stale |
| **This approach** | 🟢 Low (~500 tokens) | ✅ Current |

By extracting only essential patterns and storing them in a structured format:
- Context stays lean
- Information is task-relevant
- Can refresh anytime with `/bf:docs`
- Summaries persist for future tasks
