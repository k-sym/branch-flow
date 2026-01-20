# Branch Flow - CLAUDE.md

This project uses **Branch Flow**, a single-task, branch-based autonomous development workflow.

## Quick Start

```bash
/bf:init     # Initialize in your project
/bf:spec     # Create a new task specification
/bf:plan     # Generate implementation plan
/bf:build    # Start building (creates branch)
/bf:review   # Run QA validation
/bf:merge    # Complete and integrate
/bf:status   # Check current status
/bf:abort    # Abandon current task
/bf:search   # Semantic search
/bf:similar  # Find similar files
/bf:index    # Build search index
/bf:docs     # Fetch library documentation
/bf:ideate   # Generate improvement ideas
/bf:ideas    # List/review ideas
/bf:idea-approve  # Create GitHub issue from idea
```

## Workflow Rules

1. **One task at a time**: Complete or abort before starting new
2. **Follow the plan**: Each spec has a detailed implementation plan
3. **Commit per task**: Each plan task = one commit
4. **QA before merge**: All checks must pass
5. **Update memory**: Record learnings after completion

## Directory Structure

```
.branch-flow/
├── config.json       # Workflow configuration
├── current-task.json # Active task state
├── specs/            # Task specifications
├── plans/            # Implementation plans
└── memory/           # Persistent context
    ├── project-context.md
    ├── decisions.md
    └── learnings.md
```

## Memory System

Before starting any task, read:
- `.branch-flow/memory/project-context.md` - Architecture & conventions
- `.branch-flow/memory/decisions.md` - Past technical decisions
- `.branch-flow/memory/learnings.md` - What works, what doesn't

## Git Workflow

- **Base branch**: main (configurable)
- **Feature branches**: `bf/[spec-id]-[slug]`
- **Commits**: `[spec-id] Task [n]: [description]`
- **Merge**: Squash or no-ff merge with spec reference

## Key Principles

- **Spec-driven**: Every change starts with a specification
- **Plan-first**: Analyze codebase before coding
- **TDD-friendly**: Tests alongside implementation
- **Self-validating**: Built-in QA loop
- **Memory-aware**: Context persists across sessions

## Semantic Search

Uses local Ollama embeddings for semantic search:

```bash
/bf:search "authentication patterns"  # Search codebase + memory
/bf:similar src/auth.ts               # Find similar files
/bf:index                             # Rebuild index
```

Configure model via `BF_EMBEDDING_MODEL` env var or in config.json.

## Documentation Research

Uses Context7 MCP to fetch and summarize library docs:

```bash
/bf:docs react-query        # Fetch & summarize (~50 lines, not full docs)
/bf:docs "prisma relations" # Specific feature
```

During `/bf:plan`, automatically prompts to fetch docs for detected dependencies.
