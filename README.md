# Branch Flow

**Single-task, branch-based autonomous development workflow for Claude Code**

A simplified alternative to Auto-Claude, designed for developers who prefer:
- ✅ **Single task focus** - One task at a time, no parallel execution
- ✅ **Standard git branches** - No worktrees required
- ✅ **Spec-driven development** - Every task starts with a specification
- ✅ **Self-validating QA** - Built-in quality assurance loop
- ✅ **Memory persistence** - Context maintained across sessions

---

## Installation

### Quick Install (Interactive)

```bash
# Clone or download this repo
git clone https://github.com/yourusername/branch-flow.git

# Navigate to your project and run the installer
cd your-project
bash /path/to/branch-flow/scripts/install.sh
```

That's it! The installer automatically:
- Creates all required directories
- Copies command files to `.claude/commands/`
- Copies skill files to `.claude/skills/`
- Sets up configuration files
- Configures MCP for Context7 (if API key provided)

The installer will interactively prompt you for:

1. **Install Mode** - Team (commit to repo) or Personal (gitignore)
2. **Embedding Provider** - Ollama (recommended) or llama.cpp
3. **Embedding Model** - Choose from preset models or enter a custom one
4. **Context7 API Key** - Optional, for documentation lookup via `/bf:docs`
5. **UI/UX Pro** - Optional, for design system guidance

### Install Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **Team** | Commits Branch Flow files to the repo | Share workflow with team members |
| **Personal** | Adds Branch Flow to `.gitignore` | Personal workflow on shared repos |

```bash
# Team mode (default) - share with your team
./install.sh --team

# Personal mode - keep Branch Flow private
./install.sh --personal
```

**Personal mode gitignores:**
- `.branch-flow/` - All Branch Flow data
- `.claude/commands/bf-*` - Branch Flow commands
- `.claude/skills/branch-flow/` - Branch Flow skills

### Non-Interactive Install

```bash
# With specific options
./install.sh --model mxbai-embed-large --context7-key YOUR_API_KEY

# Use all defaults (no prompts)
./install.sh -y

# Personal mode with llama.cpp
./install.sh --personal --provider llamacpp

# Custom Ollama server
./install.sh --ollama-url http://192.168.1.100:11434
```

### Installer Options

| Option | Description |
|--------|-------------|
| `--team` | Commit Branch Flow to repo (share with team) |
| `--personal` | Add Branch Flow to .gitignore (personal use) |
| `--provider PROVIDER` | Embedding provider: `ollama` or `llamacpp` |
| `--model MODEL` | Embedding model (skips selection prompt) |
| `--ollama-url URL` | Ollama server URL (default: localhost:11434) |
| `--llamacpp-url URL` | llama.cpp server URL (default: localhost:8080) |
| `--context7-key KEY` | Context7 API key for docs lookup |
| `--uipro` | Install UI/UX Pro skill for design guidance |
| `--skip-uipro` | Skip UI/UX Pro configuration |
| `--skip-ollama` | Skip Ollama availability check |
| `--skip-context7` | Skip Context7 configuration |
| `-y, --non-interactive` | Skip all prompts, use defaults |
| `--help` | Show all options |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `BF_INSTALL_MODE` | Install mode: `team` or `personal` |
| `BF_INSTALL_UIPRO` | Set to `yes` to install UI/UX Pro |
| `BF_EMBEDDING_PROVIDER` | Provider: `ollama` or `llamacpp` |
| `BF_EMBEDDING_MODEL` | Override default embedding model |
| `BF_OLLAMA_URL` | Override Ollama URL |
| `BF_LLAMACPP_URL` | Override llama.cpp URL |
| `BF_CONTEXT7_API_KEY` | Set Context7 API key |
| `BF_INTERACTIVE` | Set to 'false' for non-interactive |

### Manual Install

1. Create directories:
```bash
mkdir -p .branch-flow/{specs,plans,docs,memory,scripts}
mkdir -p .claude/{commands,skills}
```

2. Copy the command files:
```bash
cp -r /path/to/branch-flow/.claude/commands/* .claude/commands/
cp -r /path/to/branch-flow/.claude/skills/* .claude/skills/
```

3. Copy the search script:
```bash
cp /path/to/branch-flow/scripts/bf-search.py .branch-flow/scripts/
```

4. Create config files (see Configuration below)

5. Run `/bf:init` in Claude Code

---

## Usage

### Workflow Commands

| Command | Description |
|---------|-------------|
| `/bf:init` | Initialize Branch Flow in your project |
| `/bf:spec [description]` | Create a new task specification |
| `/bf:plan` | Generate implementation plan from spec |
| `/bf:build` | Start implementation (creates feature branch) |
| `/bf:review` | Run QA validation loop |
| `/bf:merge` | Complete task and merge to base branch |
| `/bf:status` | Show current task status |
| `/bf:abort` | Abandon current task |
| `/bf:search [query]` | Semantic search across codebase & memory |
| `/bf:similar [file]` | Find files similar to a given file |
| `/bf:index` | Build/update semantic search index |
| `/bf:docs [library]` | Fetch & summarize library documentation |
| `/bf:ideate` | Analyze codebase and generate improvement ideas |
| `/bf:ideas` | List and filter generated ideas |
| `/bf:idea-approve [id]` | Create GitHub issue from idea |
| `/bf:idea-dismiss [id]` | Dismiss idea from list |

### Example Session

```bash
# Start Claude Code in your project
claude

# Initialize Branch Flow
/bf:init

# Create a new task
/bf:spec "Add user authentication with JWT tokens"
# Claude will ask clarifying questions and create the spec

# Generate implementation plan
/bf:plan
# Claude analyzes codebase and creates detailed task list

# Start building
/bf:build
# Creates branch: bf/001-add-user-auth
# Implements tasks one by one with commits

# Run QA validation
/bf:review
# Runs tests, linting, checks spec compliance
# If issues found, fix them and run again

# Complete and merge
/bf:merge
# Merges to main, updates memory, cleans up
```

---

## Workflow Phases

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   1. SPEC   │───▶│  2. PLAN    │───▶│  3. BUILD   │───▶│  4. REVIEW  │───▶│  5. MERGE   │
│             │    │             │    │             │    │             │    │             │
│ Define what │    │ Analyze &   │    │ Implement   │    │ QA loop     │    │ Integrate   │
│ to build    │    │ break down  │    │ with tests  │    │ until pass  │    │ & cleanup   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### Phase 1: SPEC
- Brainstorm with Claude about what you're building
- Define requirements (must-have, should-have, out-of-scope)
- Set clear acceptance criteria
- Save to `.branch-flow/specs/001-feature-name.md`

### Phase 2: PLAN
- Claude analyzes your codebase
- Identifies files to modify/create
- Breaks work into atomic tasks
- Creates checklist with verification steps
- Save to `.branch-flow/plans/001-plan.md`

### Phase 3: BUILD
- Creates feature branch: `bf/001-feature-name`
- Works through plan tasks one by one
- Commits after each task
- Tests as you go

### Phase 4: REVIEW
- Runs automated checks (tests, lint, types)
- Verifies all acceptance criteria
- Reviews code quality
- Loops until all checks pass

### Phase 5: MERGE
- Merges to base branch (or creates PR)
- Updates memory with learnings
- Archives completed spec
- Cleans up feature branch

---

## Semantic Search

Branch Flow includes local semantic search powered by Ollama or llama.cpp embeddings.

### Embedding Providers

| Provider | Description | Best For |
|----------|-------------|----------|
| **Ollama** | Easy setup, runs as service | Most users (recommended) |
| **llama.cpp** | Lightweight, manual server | Minimal dependencies |

### Setup with Ollama (Recommended)

1. **Install Ollama**: https://ollama.ai

2. **Start Ollama**:
   ```bash
   ollama serve
   ```

3. **Pull embedding model** (done automatically during install):
   ```bash
   ollama pull nomic-embed-text
   ```

4. **Build the index**:
   ```bash
   /bf:index
   ```

### Setup with llama.cpp

1. **Install llama.cpp**: https://github.com/ggerganov/llama.cpp

2. **Download a GGUF embedding model**:
   - [nomic-embed-text-v1.5](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF)
   - [bge-small-en-v1.5](https://huggingface.co/second-state/bge-small-en-v1.5-GGUF)
   - [all-MiniLM-L6-v2](https://huggingface.co/second-state/all-MiniLM-L6-v2-GGUF)

3. **Start the embedding server**:
   ```bash
   llama-server -m nomic-embed-text-v1.5.Q8_0.gguf --embedding --port 8080
   ```

4. **Build the index**:
   ```bash
   /bf:index
   ```

### Search Commands

```bash
# Semantic search across everything
/bf:search "authentication retry logic"

# Search only code files
/bf:search "error handling patterns" --code

# Search only memory (decisions, learnings)
/bf:search "why did we choose JWT" --memory

# Search specs and plans
/bf:search "user requirements" --specs

# Find similar files
/bf:similar src/auth/jwt.ts
```

### Changing Embedding Models

**Option 1: Environment Variable**
```bash
export BF_EMBEDDING_MODEL=mxbai-embed-large
/bf:index --rebuild
```

**Option 2: Config File**
```json
// .branch-flow/config.json
{
  "embedding": {
    "provider": "ollama",
    "model": "mxbai-embed-large",
    "dimensions": 1024
  }
}
```

### Available Ollama Models

| Model | Dimensions | Notes |
|-------|------------|-------|
| `nomic-embed-text` | 768 | Default, good balance |
| `mxbai-embed-large` | 1024 | Higher quality |
| `all-minilm` | 384 | Faster, smaller |
| `snowflake-arctic-embed` | 1024 | Good for code |
| `bge-m3` | 1024 | Multilingual support |

### Available llama.cpp Models (GGUF)

| Model | Dimensions | Download |
|-------|------------|----------|
| `nomic-embed-text-v1.5.Q8_0.gguf` | 768 | [HuggingFace](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF) |
| `bge-small-en-v1.5.Q8_0.gguf` | 384 | [HuggingFace](https://huggingface.co/second-state/bge-small-en-v1.5-GGUF) |
| `all-MiniLM-L6-v2.Q8_0.gguf` | 384 | [HuggingFace](https://huggingface.co/second-state/all-MiniLM-L6-v2-GGUF) |
| `bge-base-en-v1.5.Q8_0.gguf` | 768 | [HuggingFace](https://huggingface.co/second-state/bge-base-en-v1.5-GGUF) |

### What Gets Indexed

- **Codebase**: All source files matching configured extensions
- **Memory**: project-context.md, decisions.md, learnings.md
- **Specs**: All task specifications
- **Plans**: All implementation plans

### Configuration

Full embedding configuration in `.branch-flow/config.json`:

```json
{
  "embedding": {
    "provider": "ollama",
    "model": "nomic-embed-text",
    "dimensions": 768,
    "ollama_url": "http://localhost:11434",
    "llamacpp_url": "http://localhost:8080",
    "chunk_size": 1000,
    "chunk_overlap": 200
  },
  "index": {
    "include_extensions": [".py", ".js", ".ts", ".md", ...],
    "exclude_patterns": ["node_modules", ".git", ...],
    "max_file_size_kb": 500,
    "index_memory": true,
    "index_specs": true,
    "index_codebase": true
  }
}
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BF_INSTALL_MODE` | Install mode: `team` or `personal` | `team` |
| `BF_EMBEDDING_PROVIDER` | Provider: `ollama` or `llamacpp` | `ollama` |
| `BF_EMBEDDING_MODEL` | Embedding model name | `nomic-embed-text` |
| `BF_OLLAMA_URL` | Ollama server URL | `http://localhost:11434` |
| `BF_LLAMACPP_URL` | llama.cpp server URL | `http://localhost:8080` |
| `BF_CHUNK_SIZE` | Text chunk size | `1000` |

---

## Documentation Research (Context7)

Branch Flow integrates with Context7 MCP to fetch and summarize library documentation while keeping context lean.

### Why?

| Approach | Context Cost | Problem |
|----------|--------------|---------|
| Full docs in context | 10k+ tokens | Bloats context, slow |
| Pre-written notes | ~200 tokens | Gets stale |
| **Context7 + Extract** | ~500 tokens | Fresh, relevant, lean |

### Setup Context7 MCP

**Option 1: Global (Claude Desktop)**

Edit `~/.config/claude/claude_desktop_config.json`:
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

**Option 2: Project-level**

Create `.claude/mcp.json` in your project:
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

### Usage

```bash
# Fetch and summarize docs for a library
/bf:docs react-query

# Fetch docs for specific feature
/bf:docs "prisma relations"

# Multiple libraries
/bf:docs zod
/bf:docs "tanstack table"
```

### How It Works

1. **Fetch** - Context7 MCP retrieves latest documentation
2. **Extract** - Only relevant APIs and patterns are pulled out
3. **Summarize** - Saved to `.branch-flow/docs/[library]-ref.md` (~50-100 lines)
4. **Reference** - Plan links to the concise reference file

### Example Output

```
📚 Documentation: react-query

✅ Fetched and summarized to:
   .branch-flow/docs/react-query-ref.md

📋 Key APIs extracted:
   - useQuery
   - useMutation  
   - useQueryClient

📝 Patterns documented:
   - Basic query with loading states
   - Optimistic updates

Context saved: ~60 lines (vs ~3000 in full docs)
```

### Integration with Workflow

**During `/bf:plan`:**
```
📚 This task involves external libraries:
   - react-query (data fetching)
   - zod (validation)

Fetch latest documentation? (y/n)
> y

Fetching react-query... ✓
Fetching zod... ✓

References added to plan.
```

**During `/bf:build`:**
- Reference files are consulted, not full docs
- If more detail needed, run `/bf:docs` again
- Summaries persist for future tasks

### Reference File Format

```markdown
# react-query Quick Reference

**Fetched:** 2025-01-18
**Version:** 5.x

## Key APIs

### useQuery
```typescript
const { data, isLoading, error } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos
})
```

## Patterns

### Mutation with Optimistic Update
```typescript
// Concise pattern - just the essentials
```

## Gotchas
- [ ] queryKey must be serializable
- [ ] staleTime defaults to 0
```

---

## Ideation (AI-Generated Improvement Ideas)

Branch Flow can analyze your codebase and generate categorized improvement ideas, similar to Auto-Claude's Ideation feature.

### Generate Ideas

```bash
# Analyze codebase and generate 25 ideas (5 per category)
/bf:ideate

# Focus on one category
/bf:ideate --category security
```

### Categories

| Category | Icon | Focus Areas |
|----------|------|-------------|
| Code Quality | `</>` | Duplication, complexity, testing, linting |
| UI/UX | `✨` | Usability, accessibility, consistency |
| Security | `🔒` | Vulnerabilities, auth, data exposure |
| Documentation | `📚` | Missing docs, API docs, architecture |
| Performance | `⚡` | Slow operations, caching, optimization |

### Review Ideas

```bash
# List all ideas
/bf:ideas

# Filter by category
/bf:ideas --category security

# Filter by priority
/bf:ideas --priority high

# View specific idea details
/bf:ideas 3
```

### Example Output

```
💡 Ideation Complete!

Generated 25 improvement ideas:

   </> Code Quality     5 ideas (2 major, 3 minor)
   ✨  UI/UX            5 ideas (1 high, 3 medium, 1 low)
   🔒 Security          5 ideas (2 high, 3 medium)
   📚 Documentation     5 ideas (1 high, 2 medium, 2 low)
   ⚡ Performance       5 ideas (1 high, 2 medium, 2 low)

Top Priority:
   🔒 [HIGH] Remove hardcoded Google Maps API key from frontend
   🔒 [HIGH] Implement route guards for authenticated routes
   </> [MAJOR] Extract duplicated image capture logic into composable
```

### Create GitHub Issues

When you want to work on an idea, create a GitHub issue:

```bash
# Create issue from idea #3
/bf:idea-approve 3

# Create multiple issues at once
/bf:idea-approve 3,5,7
```

Output:
```
✅ GitHub Issue Created!

Issue:    #45
Title:    Remove hardcoded Google Maps API key from frontend code
URL:      https://github.com/user/repo/issues/45
Labels:   security, priority:high

Next steps:
  /bf:spec "Fix #45 - Remove hardcoded API key"
```

### Complete Workflow

```
/bf:ideate           → Analyze codebase, generate ideas
/bf:ideas            → Review and prioritize
/bf:idea-approve 3   → Create GitHub issue #45
/bf:spec "Fix #45"   → Create spec linked to issue
/bf:plan             → Generate implementation plan
/bf:build            → Create branch: bf/004-fix-45
/bf:merge            → PR includes "Closes #45", issue auto-closes
```

### Dismiss Ideas

```bash
# Dismiss an idea you don't want to pursue
/bf:idea-dismiss 3

# See dismissed ideas
/bf:ideas --status dismissed
```

### Ideas Storage

Ideas are stored in `.branch-flow/ideas/ideas.json`:

```json
{
  "generated_at": "2025-01-19T16:45:00Z",
  "total": 25,
  "ideas": [
    {
      "id": 1,
      "category": "security",
      "priority": "high",
      "title": "Remove hardcoded API key",
      "description": "...",
      "files": ["src/components/AuditDetail.vue"],
      "status": "pending",
      "github_issue": null
    }
  ]
}
```

---

## UI/UX Pro Skill (Optional)

Branch Flow can optionally integrate with UI/UX Pro for design system guidance when working on user interfaces.

### Installation

During Branch Flow installation, choose to install UI/UX Pro when prompted, or install manually:

```bash
# Install the CLI globally
npm install -g uipro-cli

# Initialize in your project
uipro init --ai claude
```

Or use the installer flag:
```bash
./install.sh --uipro
```

### What It Does

When installed, Claude automatically consults the UI/UX Pro skill for:

- **User Interface Design** - Component patterns, layouts, visual hierarchy
- **User Experience** - User flows, interaction patterns, feedback states
- **Visual Design** - Colors, typography, spacing, consistency
- **Accessibility** - WCAG compliance, screen reader support, keyboard navigation
- **Responsive Design** - Mobile-first patterns, breakpoints, touch targets
- **Component Patterns** - Buttons, forms, modals, tables, navigation

### CLI Commands

```bash
# Get design patterns for a component type
uipro patterns button
uipro patterns form
uipro patterns modal
uipro patterns table

# Run accessibility audit on a file
uipro a11y src/components/LoginForm.vue

# Generate accessible color palette
uipro colors "#3B82F6"

# Check design consistency
uipro check

# View spacing system
uipro spacing
```

### Integration with Workflow

The UI/UX Pro skill integrates naturally with Branch Flow:

```
/bf:ideate           → Generates UI/UX improvement ideas
/bf:spec "Redesign login form"  → Claude consults UI/UX skill
/bf:plan             → Plan includes design patterns
/bf:build            → Implementation follows design principles
/bf:review           → Checks accessibility and consistency
```

### When to Use

Claude will automatically reference the UI/UX Pro skill when you mention:
- "design", "UI", "UX", "interface", "layout"
- "component", "button", "form", "modal"
- "style", "styling", "CSS", "colors", "theme"
- "responsive", "mobile", "accessibility"
- "animation", "loading state", "empty state"

---

## Configuration

### `.branch-flow/config.json`

```json
{
  "baseBranch": "main",
  "branchPrefix": "bf/",
  "autoCommit": true,
  "requireTests": true,
  "requireLint": true,
  "autoMerge": false,
  "prTemplate": true,
  "nextSpecId": 1
}
```

| Option | Description | Default |
|--------|-------------|---------|
| `baseBranch` | Branch to create features from | `main` |
| `branchPrefix` | Prefix for feature branches | `bf/` |
| `autoCommit` | Auto-commit after each task | `true` |
| `requireTests` | Require tests to pass in review | `true` |
| `requireLint` | Require lint to pass in review | `true` |
| `autoMerge` | Merge directly (vs create PR) | `false` |
| `prTemplate` | Use PR template for merge | `true` |

---

## Memory System

Branch Flow maintains persistent context across sessions:

```
.branch-flow/memory/
├── project-context.md  # Architecture, patterns, conventions
├── decisions.md        # Technical decisions log
└── learnings.md        # What worked, what didn't
```

### Project Context
Automatically populated during `/bf:init`:
- Project overview and tech stack
- Architectural patterns
- Coding conventions
- Testing approach
- Key dependencies

### Decisions Log
Records significant technical decisions:
- Context: Why the decision was needed
- Decision: What was decided
- Rationale: Why this choice
- Consequences: Expected impact

### Learnings
Updated after each completed task:
- What worked well
- Challenges encountered
- Recommendations for similar work

---

## Directory Structure

```
your-project/
├── .branch-flow/
│   ├── config.json           # Workflow configuration
│   ├── current-task.json     # Active task state
│   ├── specs/                # Task specifications
│   │   ├── 001-add-auth.md
│   │   └── 002-fix-bug.md
│   ├── plans/                # Implementation plans
│   │   ├── 001-plan.md
│   │   └── 002-plan.md
│   ├── docs/                 # Library documentation references
│   │   └── react-query-ref.md
│   ├── memory/               # Persistent context
│   │   ├── project-context.md
│   │   ├── decisions.md
│   │   └── learnings.md
│   ├── scripts/              # Utility scripts
│   │   └── bf-search.py
│   └── index/                # Semantic search index (auto-created)
│       └── search.db
├── .claude/
│   └── commands/             # Slash commands
│       ├── bf-init.md
│       ├── bf-spec.md
│       ├── bf-plan.md
│       ├── bf-build.md
│       ├── bf-review.md
│       ├── bf-merge.md
│       ├── bf-status.md
│       ├── bf-abort.md
│       ├── bf-search.md
│       ├── bf-similar.md
│       ├── bf-index.md
│       └── bf-docs.md
└── CLAUDE.md                 # Project instructions
```

---

## Comparison with Auto-Claude

| Feature | Auto-Claude | Branch Flow |
|---------|-------------|-------------|
| Parallel tasks | Up to 12 agents | Single task |
| Git isolation | Worktrees | Branches |
| Spec-driven | ✅ | ✅ |
| QA validation | ✅ | ✅ |
| Memory layer | ✅ | ✅ |
| GUI | Desktop app | CLI only |
| Complexity | Higher | Simpler |

---

## Requirements

- **Claude Code CLI** - `npm install -g @anthropic-ai/claude-code`
- **Git repository** - Project must be a git repo
- **Claude Pro/Max** - Required for Claude Code

---

## Tips for Best Results

1. **Write detailed specs** - The more specific, the better
2. **Keep tasks small** - Break large features into multiple specs
3. **Review the plan** - Adjust before building
4. **Run QA often** - Catch issues early
5. **Update memory** - Good context improves future tasks

---

## Troubleshooting

### Ollama Issues

**"Ollama not running"**
```bash
# Start Ollama service
ollama serve

# Or on macOS, start the app
open -a Ollama
```

**"Model not found"**
```bash
# Pull the embedding model
ollama pull nomic-embed-text

# Or your configured model
ollama pull mxbai-embed-large
```

**"Connection refused to localhost:11434"**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# If using custom URL, set environment variable
export BF_OLLAMA_URL="http://your-server:11434"
```

### Search Index Issues

**"Index not found"**
```bash
# Build the index
/bf:index

# Or via Python script
python .branch-flow/scripts/bf-search.py index
```

**"Index out of date"**
```bash
# Rebuild the index
/bf:index --rebuild
```

**Search returns no results**
- Check that files match `include_extensions` in config
- Verify files aren't in `exclude_patterns`
- Rebuild index: `/bf:index --rebuild`

### Context7 MCP Issues

**"Context7 not available"**
1. Ensure MCP is configured in `.claude/mcp.json`:
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
2. Restart Claude Code after configuration

**Documentation fetch fails**
- Check internet connection
- Try a different library name
- Context7 may not have docs for that library

### Git Issues

**"Not a git repository"**
```bash
# Initialize git first
git init
git add .
git commit -m "Initial commit"

# Then run Branch Flow install
./install.sh
```

**Branch already exists**
```bash
# Delete old branch if abandoned
git branch -D bf/001-feature-name

# Or use /bf:abort to clean up properly
```

### General Issues

**Commands not found**
- Ensure `.claude/commands/` contains the bf-*.md files
- Check file permissions
- Restart Claude Code

**Config not loading**
- Verify `.branch-flow/config.json` is valid JSON
- Check for syntax errors: `python -m json.tool .branch-flow/config.json`

---

## License

MIT License - Feel free to use, modify, and distribute.

---

## Contributing

Contributions welcome! Please open an issue or PR.

---

## Acknowledgments

Inspired by [Auto-Claude](https://github.com/AndyMik90/Auto-Claude) and [obra/superpowers](https://github.com/obra/superpowers).
