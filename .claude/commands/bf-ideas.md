# List and Review Ideas

Display generated ideas with filtering and details.

## Arguments
- `$ARGUMENTS` - Optional filters:
  - `--category <cat>` or `-c <cat>` - Filter by category (code, uiux, security, docs, performance)
  - `--priority <level>` or `-p <level>` - Filter by priority (high, medium, low, major, minor)
  - `--status <status>` - Filter by status (pending, approved, dismissed)
  - `<id>` - Show details for specific idea

## Instructions

1. **Load ideas:**
   ```bash
   cat .branch-flow/ideas/ideas.json
   ```
   
   If no ideas exist:
   ```
   💡 No ideas generated yet. Run /bf:ideate to analyze your codebase.
   ```

2. **Apply filters** based on arguments

3. **Display ideas table:**

```
💡 Ideas (25 total, showing 25)

┌─────┬──────────┬──────────┬─────────────────────────────────────────────────────┐
│ ID  │ Category │ Priority │ Title                                               │
├─────┼──────────┼──────────┼─────────────────────────────────────────────────────┤
│  1  │ 🔒 Sec   │ 🔴 high  │ Remove hardcoded Google Maps API key from frontend  │
│  2  │ 🔒 Sec   │ 🔴 high  │ Implement route guards for authenticated routes     │
│  3  │ 🔒 Sec   │ 🟡 med   │ Upgrade outdated axios dependency with vulns        │
│  4  │ 🔒 Sec   │ 🟡 med   │ Remove excessive console logging of auth data       │
│  5  │ 🔒 Sec   │ 🟡 med   │ Sanitize HTML content to prevent XSS                │
│  6  │ </> Code │ 🔴 major │ Extract duplicated image capture into composable    │
│  7  │ </> Code │ 🔴 major │ Split monolithic audit store into domain stores     │
│  8  │ </> Code │ 🔴 major │ Add ESLint and Prettier for code consistency        │
│ ... │          │          │                                                     │
└─────┴──────────┴──────────┴─────────────────────────────────────────────────────┘

Filters: /bf:ideas --category security
Actions: /bf:ideas <id> for details, /bf:idea-approve <id> to create issue
```

4. **Category icons:**
   - `</>` Code Quality
   - `✨` UI/UX
   - `🔒` Security
   - `📚` Docs
   - `⚡` Performance

5. **Priority colors/icons:**
   - `🔴` high / major
   - `🟡` medium / minor
   - `🟢` low

6. **If showing single idea details** (`/bf:ideas 3`):

```
💡 Idea #3: Upgrade outdated axios dependency

Category:    🔒 Security
Priority:    🟡 medium
Effort:      small
Status:      pending
GitHub:      (not created)

Description:
The project uses axios@0.21.1 which has known security vulnerabilities 
including CVE-2021-3749 (ReDoS vulnerability) and other issues. This 
version is significantly outdated (latest is 1.x).

Files:
  • package.json

Suggested Fix:
Run `npm update axios` or `npm install axios@latest` and test all API 
calls for breaking changes. The v1.x release has some API differences.

Actions:
  /bf:idea-approve 3    Create GitHub issue
  /bf:idea-dismiss 3    Remove from list
  /bf:spec "Upgrade axios to fix CVE-2021-3749"   Start spec directly
```

## Filter Examples

```bash
# Show only security ideas
/bf:ideas --category security
/bf:ideas -c security

# Show only high priority
/bf:ideas --priority high
/bf:ideas -p high

# Combine filters
/bf:ideas -c code -p major

# Show pending only (not yet approved or dismissed)
/bf:ideas --status pending

# Show what's been approved (has GitHub issues)
/bf:ideas --status approved
```

## Quick Actions

From the ideas list, users can:

1. **View details**: `/bf:ideas 3`
2. **Create GitHub issue**: `/bf:idea-approve 3`
3. **Dismiss idea**: `/bf:idea-dismiss 3`
4. **Start spec directly**: `/bf:spec "Fix security issue from idea #3"`

## Statistics Summary

At the end of the listing, show:

```
Summary:
  Pending:   20 ideas
  Approved:   3 ideas (GitHub issues created)
  Dismissed:  2 ideas

By Priority:
  🔴 High/Major:  7 ideas
  🟡 Medium:     12 ideas
  🟢 Low:         6 ideas
```
