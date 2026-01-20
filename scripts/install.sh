#!/bin/bash

# Branch Flow Installer
# Installs the Branch Flow workflow system into your project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Determine script location (where branch-flow was downloaded/cloned)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRANCH_FLOW_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Verify branch-flow structure exists
if [ ! -d "$BRANCH_FLOW_ROOT/.claude/commands" ]; then
    echo -e "${RED}Error: Cannot find Branch Flow commands at $BRANCH_FLOW_ROOT/.claude/commands${NC}"
    echo "Please ensure the install script is run from the branch-flow distribution."
    exit 1
fi

# Default configuration
EMBEDDING_MODEL="${BF_EMBEDDING_MODEL:-}"
OLLAMA_URL="${BF_OLLAMA_URL:-http://localhost:11434}"
SKIP_OLLAMA_CHECK="${BF_SKIP_OLLAMA_CHECK:-false}"
CONTEXT7_API_KEY="${BF_CONTEXT7_API_KEY:-}"
INTERACTIVE="${BF_INTERACTIVE:-true}"
SKIP_CONTEXT7="${BF_SKIP_CONTEXT7:-false}"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --model)
            EMBEDDING_MODEL="$2"
            shift 2
            ;;
        --model=*)
            EMBEDDING_MODEL="${1#*=}"
            shift
            ;;
        --ollama-url)
            OLLAMA_URL="$2"
            shift 2
            ;;
        --ollama-url=*)
            OLLAMA_URL="${1#*=}"
            shift
            ;;
        --context7-key)
            CONTEXT7_API_KEY="$2"
            shift 2
            ;;
        --context7-key=*)
            CONTEXT7_API_KEY="${1#*=}"
            shift
            ;;
        --skip-ollama)
            SKIP_OLLAMA_CHECK="true"
            shift
            ;;
        --skip-context7)
            SKIP_CONTEXT7="true"
            shift
            ;;
        --non-interactive|-y)
            INTERACTIVE="false"
            shift
            ;;
        --help)
            echo "Branch Flow Installer"
            echo ""
            echo "Usage: install.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --model MODEL          Embedding model (interactive if not set)"
            echo "  --ollama-url URL       Ollama server URL (default: http://localhost:11434)"
            echo "  --context7-key KEY     Context7 API key for documentation lookup"
            echo "  --skip-ollama          Skip Ollama availability check"
            echo "  --skip-context7        Skip Context7 configuration"
            echo "  --non-interactive, -y  Skip all prompts, use defaults"
            echo "  --help                 Show this help message"
            echo ""
            echo "Available embedding models:"
            echo "  1. nomic-embed-text       768 dims  - Default, good balance"
            echo "  2. mxbai-embed-large      1024 dims - Higher quality"
            echo "  3. all-minilm             384 dims  - Faster, smaller"
            echo "  4. snowflake-arctic-embed 1024 dims - Good for code"
            echo "  5. bge-m3                 1024 dims - Multilingual"
            echo ""
            echo "Environment variables:"
            echo "  BF_EMBEDDING_MODEL     Override default model"
            echo "  BF_OLLAMA_URL          Override Ollama URL"
            echo "  BF_CONTEXT7_API_KEY    Context7 API key"
            echo "  BF_SKIP_OLLAMA_CHECK   Skip Ollama check if set"
            echo "  BF_SKIP_CONTEXT7       Skip Context7 setup if set"
            echo "  BF_INTERACTIVE         Set to 'false' to skip prompts"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Model options array
declare -a MODEL_NAMES=("nomic-embed-text" "mxbai-embed-large" "all-minilm" "snowflake-arctic-embed" "bge-m3")
declare -a MODEL_DIMS=(768 1024 384 1024 1024)
declare -a MODEL_DESCS=("Default, good balance" "Higher quality" "Faster, smaller" "Good for code" "Multilingual")

# Model dimensions lookup
get_model_dimensions() {
    case $1 in
        nomic-embed-text) echo 768 ;;
        mxbai-embed-large) echo 1024 ;;
        all-minilm) echo 384 ;;
        snowflake-arctic-embed) echo 1024 ;;
        bge-m3) echo 1024 ;;
        *) echo 768 ;;  # Default
    esac
}

# Interactive model selection
select_embedding_model() {
    echo ""
    echo -e "${BOLD}Select Embedding Model for Semantic Search:${NC}"
    echo ""
    echo -e "  ${CYAN}1)${NC} nomic-embed-text       ${YELLOW}768 dims${NC}  - Default, good balance"
    echo -e "  ${CYAN}2)${NC} mxbai-embed-large      ${YELLOW}1024 dims${NC} - Higher quality"
    echo -e "  ${CYAN}3)${NC} all-minilm             ${YELLOW}384 dims${NC}  - Faster, smaller"
    echo -e "  ${CYAN}4)${NC} snowflake-arctic-embed ${YELLOW}1024 dims${NC} - Good for code"
    echo -e "  ${CYAN}5)${NC} bge-m3                 ${YELLOW}1024 dims${NC} - Multilingual"
    echo -e "  ${CYAN}6)${NC} Custom model name"
    echo ""
    read -p "Enter choice [1-6] (default: 1): " model_choice
    
    case $model_choice in
        1|"") EMBEDDING_MODEL="nomic-embed-text" ;;
        2) EMBEDDING_MODEL="mxbai-embed-large" ;;
        3) EMBEDDING_MODEL="all-minilm" ;;
        4) EMBEDDING_MODEL="snowflake-arctic-embed" ;;
        5) EMBEDDING_MODEL="bge-m3" ;;
        6)
            read -p "Enter custom model name: " custom_model
            if [ -n "$custom_model" ]; then
                EMBEDDING_MODEL="$custom_model"
                read -p "Enter embedding dimensions (default: 768): " custom_dims
                CUSTOM_DIMENSIONS="${custom_dims:-768}"
            else
                EMBEDDING_MODEL="nomic-embed-text"
            fi
            ;;
        *)
            echo -e "${YELLOW}Invalid choice, using default: nomic-embed-text${NC}"
            EMBEDDING_MODEL="nomic-embed-text"
            ;;
    esac
    
    echo -e "${GREEN}✓ Selected: $EMBEDDING_MODEL${NC}"
}

# Interactive Context7 setup
setup_context7() {
    echo ""
    echo -e "${BOLD}Context7 MCP Configuration (for documentation lookup):${NC}"
    echo ""
    echo "Context7 provides AI-powered documentation search for libraries."
    echo "Get your API key at: https://context7.com"
    echo ""
    read -p "Do you want to configure Context7? [y/N]: " setup_c7
    
    if [[ "$setup_c7" =~ ^[Yy]$ ]]; then
        read -p "Enter Context7 API key (or press Enter to skip): " c7_key
        if [ -n "$c7_key" ]; then
            CONTEXT7_API_KEY="$c7_key"
            echo -e "${GREEN}✓ Context7 API key configured${NC}"
        else
            echo -e "${YELLOW}Skipped - you can add it later to .claude/mcp.json${NC}"
        fi
    else
        echo -e "${YELLOW}Skipped - you can configure Context7 later${NC}"
    fi
}

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════╗"
echo "║         Branch Flow Installer            ║"
echo "║   Single-Task Autonomous Development     ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${NC}"

# Interactive prompts (if not in non-interactive mode)
if [ "$INTERACTIVE" = "true" ]; then
    # Model selection (if not already set)
    if [ -z "$EMBEDDING_MODEL" ]; then
        select_embedding_model
    fi
    
    # Context7 setup (if not skipped and no key provided)
    if [ "$SKIP_CONTEXT7" != "true" ] && [ -z "$CONTEXT7_API_KEY" ]; then
        setup_context7
    fi
fi

# Apply defaults if still empty
if [ -z "$EMBEDDING_MODEL" ]; then
    EMBEDDING_MODEL="nomic-embed-text"
fi

# Calculate dimensions (use custom if set, otherwise lookup)
if [ -n "$CUSTOM_DIMENSIONS" ]; then
    EMBEDDING_DIMENSIONS="$CUSTOM_DIMENSIONS"
else
    EMBEDDING_DIMENSIONS=$(get_model_dimensions "$EMBEDDING_MODEL")
fi

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo -e "${RED}Error: Not a git repository${NC}"
    echo "Please run this from within a git repository."
    exit 1
fi

# Get project root
PROJECT_ROOT=$(git rev-parse --show-toplevel)
cd "$PROJECT_ROOT"

echo -e "${YELLOW}Installing to: $PROJECT_ROOT${NC}"
echo ""

# Detect base branch
if git show-ref --verify --quiet refs/heads/main; then
    BASE_BRANCH="main"
elif git show-ref --verify --quiet refs/heads/master; then
    BASE_BRANCH="master"
else
    BASE_BRANCH="main"
fi

echo -e "${GREEN}✓ Detected base branch: $BASE_BRANCH${NC}"

# Create directory structure
echo -e "${BLUE}Creating directory structure...${NC}"

mkdir -p .branch-flow/{specs,plans,docs,memory,scripts,ideas}
mkdir -p .claude/commands
mkdir -p .claude/skills

echo -e "${GREEN}✓ Created .branch-flow/ directories${NC}"
echo -e "${GREEN}✓ Created .claude/ directories${NC}"

# Copy command files from branch-flow distribution
echo -e "${BLUE}Installing command files...${NC}"

if [ -d "$BRANCH_FLOW_ROOT/.claude/commands" ]; then
    cp -r "$BRANCH_FLOW_ROOT/.claude/commands/"* .claude/commands/ 2>/dev/null || true
    COMMANDS_COPIED=$(ls -1 .claude/commands/*.md 2>/dev/null | wc -l)
    echo -e "${GREEN}✓ Copied $COMMANDS_COPIED command files to .claude/commands/${NC}"
else
    echo -e "${YELLOW}⚠ Command files not found in distribution${NC}"
fi

# Copy skill files if present
if [ -d "$BRANCH_FLOW_ROOT/.claude/skills" ]; then
    cp -r "$BRANCH_FLOW_ROOT/.claude/skills/"* .claude/skills/ 2>/dev/null || true
    echo -e "${GREEN}✓ Copied skill files to .claude/skills/${NC}"
fi

# Create config file
echo -e "${BLUE}Creating configuration...${NC}"

cat > .branch-flow/config.json << EOF
{
  "baseBranch": "$BASE_BRANCH",
  "branchPrefix": "bf/",
  "autoCommit": true,
  "requireTests": true,
  "requireLint": true,
  "autoMerge": false,
  "prTemplate": true,
  "nextSpecId": 1,
  "embedding": {
    "provider": "ollama",
    "model": "$EMBEDDING_MODEL",
    "dimensions": $EMBEDDING_DIMENSIONS,
    "ollama_url": "$OLLAMA_URL",
    "batch_size": 10,
    "chunk_size": 1000,
    "chunk_overlap": 200
  },
  "index": {
    "include_extensions": [
      ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java",
      ".cpp", ".c", ".h", ".hpp", ".cs", ".rb", ".php", ".swift",
      ".kt", ".scala", ".md", ".txt", ".json", ".yaml", ".yml"
    ],
    "exclude_patterns": [
      "node_modules", ".git", "__pycache__", ".branch-flow/index",
      "dist", "build", ".next", "target", "vendor", ".venv", "venv",
      ".cache", "coverage", ".nyc_output", ".pytest_cache", ".claude",
      ".cursor", ".vscode", ".quasar", ".idea", ".eclipse"
    ],
    "exclude_files": [
      "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "composer.lock",
      "Gemfile.lock", "Cargo.lock", "poetry.lock", "Pipfile.lock",
      ".DS_Store", ".gitignore", ".editorconfig"
    ],
    "max_file_size_kb": 500,
    "index_memory": true,
    "index_specs": true,
    "index_codebase": true
  }
}
EOF

echo -e "${GREEN}✓ Created config.json${NC}"
echo -e "   Embedding model: ${CYAN}$EMBEDDING_MODEL${NC} ($EMBEDDING_DIMENSIONS dims)"

# Create current-task.json
cat > .branch-flow/current-task.json << EOF
{
  "specId": null,
  "status": "idle",
  "lastCompleted": null
}
EOF

echo -e "${GREEN}✓ Created current-task.json${NC}"

# Create MCP config for Context7 if API key provided
if [ -n "$CONTEXT7_API_KEY" ]; then
    mkdir -p .claude
    cat > .claude/mcp.json << EOF
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp"],
      "env": {
        "CONTEXT7_API_KEY": "$CONTEXT7_API_KEY"
      }
    }
  }
}
EOF
    echo -e "${GREEN}✓ Created .claude/mcp.json with Context7 configuration${NC}"
else
    # Create MCP config without API key (user can add later)
    if [ ! -f .claude/mcp.json ]; then
        mkdir -p .claude
        cat > .claude/mcp.json << 'EOF'
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp"],
      "env": {
        "CONTEXT7_API_KEY": ""
      }
    }
  }
}
EOF
        echo -e "${YELLOW}✓ Created .claude/mcp.json (add your Context7 API key to enable docs lookup)${NC}"
    fi
fi

# Create memory files
cat > .branch-flow/memory/project-context.md << 'EOF'
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
*Last updated: Run /bf:init to auto-populate*
EOF

cat > .branch-flow/memory/decisions.md << 'EOF'
# Technical Decisions

A log of significant technical decisions made during development.

## Template

### [Date] - [Decision Title]
**Context:** Why this decision was needed
**Decision:** What was decided
**Rationale:** Why this choice was made
**Consequences:** Expected impact

---
EOF

cat > .branch-flow/memory/learnings.md << 'EOF'
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
EOF

echo -e "${GREEN}✓ Created memory files${NC}"

# Copy commands (these would be copied from the branch-flow source)
# For now, we'll create a note about where to get them

echo -e "${BLUE}Setting up slash commands...${NC}"

# Note: In practice, these would be copied from the branch-flow package
# For this demo, we're just noting they need to be installed

cat > .claude/commands/README.md << 'EOF'
# Branch Flow Commands

These commands are part of the Branch Flow workflow system.

## Available Commands

- `/bf:init` - Initialize Branch Flow
- `/bf:spec` - Create task specification
- `/bf:plan` - Generate implementation plan
- `/bf:build` - Start implementation
- `/bf:review` - Run QA validation
- `/bf:merge` - Complete and integrate
- `/bf:status` - Show current status
- `/bf:abort` - Abandon task

## Installation

Copy the command files from the branch-flow package to this directory,
or install the branch-flow plugin:

```bash
# If using Claude Code plugin system
/plugin install branch-flow

# Or manually copy from:
# https://github.com/your-repo/branch-flow/.claude/commands/
```
EOF

echo -e "${GREEN}✓ Commands directory ready${NC}"

# Create/update CLAUDE.md
if [ -f "CLAUDE.md" ]; then
    echo -e "${YELLOW}CLAUDE.md exists - appending Branch Flow section${NC}"
    echo "" >> CLAUDE.md
    echo "---" >> CLAUDE.md
    echo "" >> CLAUDE.md
    cat << 'EOF' >> CLAUDE.md

## Branch Flow

This project uses Branch Flow for autonomous development.

Commands: `/bf:init`, `/bf:spec`, `/bf:plan`, `/bf:build`, `/bf:review`, `/bf:merge`, `/bf:status`, `/bf:abort`

See `.branch-flow/` for specs, plans, and memory.
EOF
else
    cat > CLAUDE.md << 'EOF'
# Project Instructions

## Branch Flow

This project uses **Branch Flow**, a single-task, branch-based autonomous development workflow.

### Quick Start

```
/bf:init     # Initialize (already done)
/bf:spec     # Create a new task
/bf:plan     # Generate implementation plan
/bf:build    # Start building
/bf:review   # Run QA validation
/bf:merge    # Complete and integrate
```

### Directory Structure

```
.branch-flow/
├── config.json       # Configuration
├── current-task.json # Active task state
├── specs/            # Task specifications
├── plans/            # Implementation plans
└── memory/           # Persistent context
```

### Workflow

1. One task at a time
2. Every task has a spec and plan
3. QA validation before merge
4. Memory updated after completion
EOF
fi

echo -e "${GREEN}✓ Updated CLAUDE.md${NC}"

# Update .gitignore
if [ -f ".gitignore" ]; then
    if ! grep -q ".branch-flow/current-task.json" .gitignore; then
        echo "" >> .gitignore
        echo "# Branch Flow" >> .gitignore
        echo ".branch-flow/current-task.json" >> .gitignore
        echo ".branch-flow/index/" >> .gitignore
        echo -e "${GREEN}✓ Updated .gitignore${NC}"
    fi
else
    echo "# Branch Flow" > .gitignore
    echo ".branch-flow/current-task.json" >> .gitignore
    echo ".branch-flow/index/" >> .gitignore
    echo -e "${GREEN}✓ Created .gitignore${NC}"
fi

# Create scripts directory and copy search script
mkdir -p .branch-flow/scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/bf-search.py" ]; then
    cp "$SCRIPT_DIR/bf-search.py" .branch-flow/scripts/
    chmod +x .branch-flow/scripts/bf-search.py
    echo -e "${GREEN}✓ Installed semantic search script${NC}"
fi

# Check Ollama availability
echo ""
if [ "$SKIP_OLLAMA_CHECK" != "true" ]; then
    echo -e "${BLUE}Checking Ollama availability...${NC}"
    
    if command -v ollama &> /dev/null; then
        echo -e "${GREEN}✓ Ollama is installed${NC}"
        
        # Check if Ollama is running
        if curl -s "$OLLAMA_URL/api/version" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Ollama is running at $OLLAMA_URL${NC}"
            
            # Check if model is available
            if ollama list 2>/dev/null | grep -q "$EMBEDDING_MODEL"; then
                echo -e "${GREEN}✓ Model $EMBEDDING_MODEL is available${NC}"
            else
                echo -e "${YELLOW}⚠ Model $EMBEDDING_MODEL not found. Pulling...${NC}"
                ollama pull "$EMBEDDING_MODEL" || echo -e "${RED}  Failed to pull model. Run manually: ollama pull $EMBEDDING_MODEL${NC}"
            fi
        else
            echo -e "${YELLOW}⚠ Ollama is not running${NC}"
            echo -e "  Start it with: ${CYAN}ollama serve${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ Ollama is not installed${NC}"
        echo -e "  Install from: ${CYAN}https://ollama.ai${NC}"
        echo -e "  Then run: ${CYAN}ollama pull $EMBEDDING_MODEL${NC}"
    fi
else
    echo -e "${YELLOW}Skipping Ollama check (--skip-ollama)${NC}"
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Branch Flow installed successfully!  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "📁 Created:"
echo -e "   .branch-flow/"
echo -e "   ├── config.json"
echo -e "   ├── current-task.json"
echo -e "   ├── scripts/"
echo -e "   │   └── bf-search.py"
echo -e "   ├── specs/"
echo -e "   ├── plans/"
echo -e "   ├── docs/"
echo -e "   └── memory/"
echo -e "       ├── project-context.md"
echo -e "       ├── decisions.md"
echo -e "       └── learnings.md"
echo -e "   .claude/"
echo -e "   ├── commands/        (${COMMANDS_COPIED} commands)"
echo -e "   ├── skills/"
echo -e "   └── mcp.json"
echo ""
echo -e "🔧 Configuration:"
echo -e "   Base branch: ${BLUE}$BASE_BRANCH${NC}"
echo -e "   Branch prefix: ${BLUE}bf/${NC}"
echo -e "   Embedding model: ${BLUE}$EMBEDDING_MODEL${NC} ($EMBEDDING_DIMENSIONS dims)"
if [ -n "$CONTEXT7_API_KEY" ]; then
    echo -e "   Context7: ${GREEN}Configured ✓${NC}"
else
    echo -e "   Context7: ${YELLOW}Not configured (add API key to .claude/mcp.json)${NC}"
fi
echo ""
echo -e "🔍 Semantic Search:"
echo -e "   To change models, set ${CYAN}BF_EMBEDDING_MODEL${NC} or use:"
echo -e "   ${CYAN}python .branch-flow/scripts/bf-search.py config --set-model <model>${NC}"
echo ""
echo -e "📚 Documentation Lookup (Context7):"
if [ -n "$CONTEXT7_API_KEY" ]; then
    echo -e "   ${GREEN}Ready to use!${NC} Run ${BLUE}/bf:docs <library>${NC}"
else
    echo -e "   Get your API key at: ${CYAN}https://context7.com${NC}"
    echo -e "   Add to .claude/mcp.json or run: ${CYAN}export BF_CONTEXT7_API_KEY=your-key${NC}"
fi
echo ""
echo -e "📝 Next steps:"
echo -e "   1. Ensure Ollama is running: ${CYAN}ollama serve${NC}"
echo -e "   2. Run ${BLUE}/bf:init${NC} to analyze your codebase"
echo -e "   3. Run ${BLUE}/bf:index${NC} to build search index"
echo -e "   4. Create your first spec with ${BLUE}/bf:spec${NC}"
echo ""
echo -e "📚 Commands:"
echo -e "   /bf:init    - Initialize project context"
echo -e "   /bf:spec    - Create task specification"
echo -e "   /bf:plan    - Generate implementation plan"
echo -e "   /bf:build   - Start implementation"
echo -e "   /bf:review  - Run QA validation"
echo -e "   /bf:merge   - Complete and merge"
echo -e "   /bf:search  - Semantic search"
echo -e "   /bf:similar - Find similar files"
echo -e "   /bf:index   - Rebuild search index"
echo -e "   /bf:docs    - Fetch library documentation"
echo ""
