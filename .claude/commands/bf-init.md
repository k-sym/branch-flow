# Initialize Branch Flow

Initialize the Branch Flow workflow system in the current project.

## Prerequisites

- Git repository (will check and error if not)
- Ollama installed (optional, for semantic search)

## Instructions

1. **Verify Git Repository**
   ```bash
   git rev-parse --is-inside-work-tree
   ```
   Exit with helpful message if not a git repo.

2. **Detect Base Branch**
   Check for `main` or `master`, default to `main` if neither exists.

3. **Create Directory Structure**
   ```bash
   mkdir -p .branch-flow/{specs,plans,docs,memory,scripts,ideas}
   mkdir -p .claude/commands
   ```

4. **Create Configuration File** `.branch-flow/config.json`:
   ```json
   {
     "baseBranch": "main",
     "branchPrefix": "bf/",
     "autoCommit": true,
     "requireTests": true,
     "requireLint": true,
     "autoMerge": false,
     "prTemplate": true,
     "nextSpecId": 1,
     "embedding": {
       "provider": "ollama",
       "model": "nomic-embed-text",
       "dimensions": 768,
       "ollama_url": "http://localhost:11434",
       "chunk_size": 1000,
       "chunk_overlap": 200
     },
     "index": {
       "include_extensions": [".py", ".js", ".ts", ".tsx", ".md", "..."],
       "exclude_patterns": ["node_modules", ".git", "..."],
       "max_file_size_kb": 500,
       "index_memory": true,
       "index_specs": true,
       "index_codebase": true
     }
   }
   ```

5. **Create Task State File** `.branch-flow/current-task.json`:
   ```json
   {
     "specId": null,
     "status": "idle",
     "lastCompleted": null
   }
   ```

6. **Create Memory Files**

   **`.branch-flow/memory/project-context.md`:**
   ```markdown
   # Project Context

   ## Overview
   [Analyze and describe the project - what it does, tech stack, structure]

   ## Architecture
   [Key architectural patterns and decisions]

   ## Conventions
   [Coding standards, naming conventions, file organization]

   ## Testing
   [Test framework, coverage requirements, testing patterns]

   ## Dependencies
   [Key dependencies and their purposes]

   ---
   *Last updated: [date]*
   ```

   **`.branch-flow/memory/decisions.md`:**
   ```markdown
   # Technical Decisions

   A log of significant technical decisions made during development.

   ## Template
   ### [Date] - [Decision Title]
   **Context:** Why this decision was needed
   **Decision:** What was decided
   **Rationale:** Why this choice was made
   **Consequences:** Expected impact

   ---
   ```

   **`.branch-flow/memory/learnings.md`:**
   ```markdown
   # Learnings

   Insights and lessons learned from completed tasks.

   ## What Works Well
   - [patterns that succeed]

   ## What to Avoid
   - [patterns that cause issues]

   ## Tips & Tricks
   - [useful techniques discovered]

   ---
   *Updated after each completed task*
   ```

7. **Copy Search Script** (if using install.sh)
   ```bash
   cp /path/to/bf-search.py .branch-flow/scripts/
   ```

8. **Update .gitignore**
   ```
   # Branch Flow
   .branch-flow/current-task.json
   .branch-flow/index/
   ```

9. **Analyze Codebase** (auto-populate project context):
   - Examine package.json, requirements.txt, Cargo.toml, etc.
   - Look at existing test structure
   - Identify main frameworks and patterns
   - Note any existing CLAUDE.md or similar files

10. **Output Summary**
    ```
    ✅ Branch Flow initialized!

    📁 Created:
       .branch-flow/
       ├── config.json
       ├── current-task.json
       ├── specs/
       ├── plans/
       ├── docs/
       ├── scripts/
       │   └── bf-search.py
       └── memory/
           ├── project-context.md
           ├── decisions.md
           └── learnings.md

    🔧 Configuration:
       Base branch: main
       Branch prefix: bf/
       Embedding model: nomic-embed-text
       
    📝 Next steps:
       1. Review .branch-flow/memory/project-context.md
       2. Start Ollama: ollama serve
       3. Build search index: /bf:index
       4. (Optional) Configure Context7 MCP for docs
       5. Create your first spec: /bf:spec
    ```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `baseBranch` | Branch to create features from | `main` |
| `branchPrefix` | Prefix for feature branches | `bf/` |
| `autoCommit` | Auto-commit after each task | `true` |
| `requireTests` | Require tests to pass in review | `true` |
| `requireLint` | Require lint to pass in review | `true` |
| `autoMerge` | Merge directly vs create PR | `false` |
| `prTemplate` | Use PR template for merge | `true` |
| `embedding.model` | Ollama embedding model | `nomic-embed-text` |

## Environment Variables

These override config.json values:

| Variable | Description |
|----------|-------------|
| `BF_EMBEDDING_MODEL` | Embedding model name |
| `BF_OLLAMA_URL` | Ollama server URL |

## Notes

- The `docs/` folder is for Context7 documentation references
- The `index/` folder (created by /bf:index) stores the search database
- Run `/bf:index` after init to enable semantic search
