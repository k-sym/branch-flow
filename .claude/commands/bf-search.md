# Semantic Search

Search the codebase, memory, and specs using semantic similarity.

## Arguments
- `$ARGUMENTS` - The search query (required)

## Instructions

1. Parse the query from arguments

2. Check if index exists:
   ```bash
   test -f .branch-flow/index/search.db || echo "Index not found"
   ```
   
   If not found:
   ```
   ⚠️ Search index not found. Building now...
   ```
   Then run `/bf:index` first.

3. Run the search:
   ```bash
   python .branch-flow/scripts/bf-search.py search "$ARGUMENTS" --limit 10
   ```

4. For type-filtered search, parse flags:
   - `--code` or `-c`: Only search codebase
   - `--memory` or `-m`: Only search memory files
   - `--specs` or `-s`: Only search specs and plans
   
   ```bash
   python .branch-flow/scripts/bf-search.py search "authentication" --type code
   ```

5. Output format:
   ```
   🔍 Search: "authentication retry logic"
   
   Found 8 relevant results:
   
   1. [code] src/auth/retry.ts:15-42
      Score: 94.2%
      Implements exponential backoff retry logic for failed auth attempts...
      
   2. [memory] .branch-flow/memory/decisions.md:45-58
      Score: 87.5%
      Decision to use exponential backoff with jitter for auth retries...
      
   3. [spec] .branch-flow/specs/001-add-auth.md:23-35
      Score: 82.1%
      Requirement: Implement retry logic with configurable attempts...
      
   4. [code] src/utils/retry.ts:1-28
      Score: 78.9%
      Generic retry utility function with customizable delay...
   
   ---
   View a result? Enter number (1-8) or press Enter to continue
   ```

6. If user selects a result, show full context:
   ```bash
   # Read the file and show surrounding context
   sed -n '15,42p' src/auth/retry.ts
   ```

## Usage Examples

```bash
# Basic search
/bf:search authentication patterns

# Search only code
/bf:search authentication --code

# Search only memory (decisions, learnings, context)
/bf:search error handling --memory

# Search specs and plans
/bf:search user requirements --specs

# Find implementation examples
/bf:search "how do we handle API errors"

# Search for patterns
/bf:search singleton pattern implementation
```

## Tips for Better Results

- **Be specific**: "JWT token refresh logic" > "tokens"
- **Use natural language**: "how do we handle failed logins"
- **Describe the concept**: "retry with exponential backoff"
- **Filter by type** when you know where to look

## Integration with Workflow

Search is automatically available during:
- `/bf:plan` - Find related implementations
- `/bf:build` - Reference similar patterns
- `/bf:review` - Check for inconsistencies

You can also invoke it directly anytime:
```
"Search for how we've implemented caching before"
→ Runs semantic search and shows relevant code
```
