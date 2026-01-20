# Find Similar Files

Find files semantically similar to a given file.

## Arguments
- `$ARGUMENTS` - Path to the file to find similar files for

## Instructions

1. Parse the file path from arguments

2. Verify the file exists:
   ```bash
   test -f "$ARGUMENTS" || echo "File not found: $ARGUMENTS"
   ```

3. Check if index exists, build if needed:
   ```bash
   test -f .branch-flow/index/search.db || python .branch-flow/scripts/bf-search.py index
   ```

4. Run similarity search:
   ```bash
   python .branch-flow/scripts/bf-search.py similar "$ARGUMENTS" --limit 10
   ```

5. Output format:
   ```
   📄 Finding files similar to: src/auth/jwt.ts
   
   Similar files found:
   
   1. [code] src/auth/token-refresh.ts
      Similarity: 89.3%
      Token refresh logic with similar JWT handling patterns
      
   2. [code] src/middleware/auth-middleware.ts
      Similarity: 82.7%
      Authentication middleware using JWT verification
      
   3. [spec] .branch-flow/specs/001-add-auth.md
      Similarity: 76.4%
      Specification that defined JWT implementation requirements
      
   4. [memory] .branch-flow/memory/decisions.md
      Similarity: 71.2%
      Decision log entry about JWT token structure
   
   ---
   View a file? Enter number (1-10) or press Enter to continue
   ```

6. If user selects a result, show the file or relevant section

## Usage Examples

```bash
# Find files similar to a specific file
/bf:similar src/auth/jwt.ts

# Find patterns similar to a utility
/bf:similar src/utils/retry.ts

# Find specs related to an implementation
/bf:similar src/api/users.ts
```

## Use Cases

### 1. Maintain Consistency
When implementing a new feature, find similar implementations to follow the same patterns:
```
/bf:similar src/api/products.ts
→ Shows: src/api/users.ts, src/api/orders.ts
→ Follow the same API structure
```

### 2. Find Related Tests
```
/bf:similar src/auth/auth.ts
→ Shows: src/auth/auth.test.ts
→ Reference existing test patterns
```

### 3. Discover Connections
```
/bf:similar src/models/user.ts
→ Shows: related services, controllers, and specs
→ Understand the dependency graph
```

### 4. Refactoring Impact
Before refactoring, find all similar code that might need updating:
```
/bf:similar src/utils/deprecated-helper.ts
→ Shows files using similar patterns
→ Update them all consistently
```

## Integration with Workflow

This command is particularly useful during:

- **Planning**: Find similar features as reference
- **Building**: Ensure consistency with existing code
- **Review**: Check if similar code needs similar fixes
