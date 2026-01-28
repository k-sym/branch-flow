# Build Search Index

Build or update the semantic search index for the codebase, memory, and specs.

## Arguments
- `$ARGUMENTS` - Optional: `--rebuild` to force full rebuild, `--quiet` for minimal output

## Instructions

1. Check if Ollama is running:
   ```bash
   curl -s http://localhost:11434/api/version || echo "Ollama not running"
   ```
   
   If not running, inform the user:
   ```
   ⚠️ Ollama is not running. Please start it:
   
   ollama serve
   
   Then run /bf:index again.
   ```

2. Check if the embedding model is available:
   ```bash
   ollama list | grep -q "nomic-embed-text" || ollama pull nomic-embed-text
   ```
   
   The model can be configured in `.branch-flow/config.json` or via environment variable `BF_EMBEDDING_MODEL`.

3. Run the indexing script:
   ```bash
   python .branch-flow/scripts/bf-search.py index
   ```

4. If `--rebuild` flag is passed, delete existing index first:
   ```bash
   rm -rf .branch-flow/index/
   python .branch-flow/scripts/bf-search.py index
   ```

5. Output:
   ```
   🔍 Building search index...
   
   📊 Configuration:
      Model: nomic-embed-text (768 dimensions)
      Provider: ollama
   
   📁 Indexing:
      src/auth/auth.ts ✓
      src/auth/auth.test.ts ✓
      .branch-flow/memory/project-context.md ✓
      .branch-flow/memory/decisions.md ✓
      .branch-flow/specs/001-add-auth.md ✓
      ... 
   
   ✅ Index complete!
      Files indexed: 45
      Total chunks: 128
      Index size: 2.3 MB
   
   Use /bf:search "query" to search
   ```

## Configuration

The embedding provider and model can be configured via:

### Embedding Providers

| Provider | Description | Setup |
|----------|-------------|-------|
| `ollama` | Easy setup, runs as service | `ollama serve` then `ollama pull <model>` |
| `llamacpp` | Lightweight, manual server | `llama-server -m <model.gguf> --embedding` |

### Option 1: config.json
```json
{
  "embedding": {
    "provider": "ollama",
    "model": "nomic-embed-text",
    "dimensions": 768,
    "ollama_url": "http://localhost:11434",
    "llamacpp_url": "http://localhost:8080"
  }
}
```

### Option 2: Environment Variables
```bash
# For Ollama
export BF_EMBEDDING_PROVIDER="ollama"
export BF_EMBEDDING_MODEL="nomic-embed-text"
export BF_OLLAMA_URL="http://localhost:11434"

# For llama.cpp
export BF_EMBEDDING_PROVIDER="llamacpp"
export BF_EMBEDDING_MODEL="nomic-embed-text-v1.5.Q8_0.gguf"
export BF_LLAMACPP_URL="http://localhost:8080"
```

### Available Ollama Models
| Model | Dimensions | Notes |
|-------|------------|-------|
| nomic-embed-text | 768 | Default, good balance |
| mxbai-embed-large | 1024 | Higher quality |
| all-minilm | 384 | Faster, smaller |
| snowflake-arctic-embed | 1024 | Good for code |
| bge-m3 | 1024 | Multilingual |

### Available llama.cpp Models (GGUF)
| Model | Dimensions | Download |
|-------|------------|----------|
| nomic-embed-text-v1.5.Q8_0.gguf | 768 | [HuggingFace](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF) |
| bge-small-en-v1.5.Q8_0.gguf | 384 | [HuggingFace](https://huggingface.co/second-state/bge-small-en-v1.5-GGUF) |
| all-MiniLM-L6-v2.Q8_0.gguf | 384 | [HuggingFace](https://huggingface.co/second-state/all-MiniLM-L6-v2-GGUF) |
| bge-base-en-v1.5.Q8_0.gguf | 768 | [HuggingFace](https://huggingface.co/second-state/bge-base-en-v1.5-GGUF) |

To change models:
```bash
# Ollama
ollama pull mxbai-embed-large
# Then update config.json

# llama.cpp
# Download GGUF file, update config.json, restart server
```

## Excluded Files

The following are automatically excluded from indexing:

**Patterns (directories):**
- `node_modules`, `.git`, `__pycache__`, `dist`, `build`
- `.next`, `target`, `vendor`, `.venv`, `venv`
- `.cache`, `coverage`, `.nyc_output`, `.pytest_cache`
- `.claude`, `.cursor`, `.vscode`, `.quasar`, `.idea`, `.eclipse`

**Lock files & config:**
- `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- `composer.lock`, `Gemfile.lock`, `Cargo.lock`
- `poetry.lock`, `Pipfile.lock`
- `.DS_Store`, `.gitignore`, `.editorconfig`

**Size limit:** Files over 500KB are skipped by default.

To customize, edit `.branch-flow/config.json`:
```json
{
  "index": {
    "exclude_patterns": ["node_modules", "..."],
    "exclude_files": ["package-lock.json", "..."],
    "max_file_size_kb": 500
  }
}
```

## Troubleshooting

**Error: HTTP 500 from Ollama**
- Usually caused by very large files. Check if a lock file slipped through.
- Indexing will continue with other files and report errors at the end.

**Error: Ollama not running**
```bash
ollama serve
```

**Error: Model not found (Ollama)**
```bash
ollama pull nomic-embed-text
```

**Error: llama.cpp server not available**
```bash
# Start the server with embedding support
llama-server -m nomic-embed-text-v1.5.Q8_0.gguf --embedding --port 8080
```

**Error: llama.cpp connection refused**
- Check the server is running: `curl http://localhost:8080/health`
- Verify port matches config: check `llamacpp_url` in config.json

**Search returns no results**
- Run `/bf:index --rebuild` to force full reindex
- Check that files match `include_extensions` in config

## When to Re-index

The index automatically detects changed files, but you should rebuild when:
- Changing embedding models
- After major refactoring
- If search results seem stale

## Automatic Indexing

The index is automatically updated:
- After `/bf:merge` completes
- When running `/bf:plan` (indexes memory)
- Manually via `/bf:index`
