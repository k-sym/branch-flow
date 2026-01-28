#!/usr/bin/env python3
"""
Branch Flow - Semantic Search Module

Uses local embeddings via Ollama for semantic search across:
- Codebase files
- Memory (decisions, learnings, context)
- Completed specs and plans

Supports multiple embedding models via configuration.
"""

import os
import json
import hashlib
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import argparse

# =============================================================================
# Configuration
# =============================================================================

DEFAULT_CONFIG = {
    "embedding": {
        "provider": "ollama",  # ollama or llamacpp
        "model": "nomic-embed-text",
        "dimensions": 768,
        "ollama_url": "http://localhost:11434",
        "llamacpp_url": "http://localhost:8080",
        "batch_size": 10,
        "chunk_size": 1000,
        "chunk_overlap": 200
    },
    "index": {
        "include_extensions": [
            ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java",
            ".cpp", ".c", ".h", ".hpp", ".cs", ".rb", ".php", ".swift",
            ".kt", ".scala", ".md", ".txt", ".json", ".yaml", ".yml",
            ".toml", ".sql", ".sh", ".bash"
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
            ".DS_Store", ".gitignore", ".editorconfig", "thumbs.db"
        ],
        "max_file_size_kb": 500,
        "index_memory": True,
        "index_specs": True,
        "index_codebase": True
    }
}

# Model presets for easy switching
# Ollama models
MODEL_PRESETS = {
    "nomic-embed-text": {
        "provider": "ollama",
        "model": "nomic-embed-text",
        "dimensions": 768
    },
    "mxbai-embed-large": {
        "provider": "ollama",
        "model": "mxbai-embed-large",
        "dimensions": 1024
    },
    "all-minilm": {
        "provider": "ollama",
        "model": "all-minilm",
        "dimensions": 384
    },
    "snowflake-arctic-embed": {
        "provider": "ollama",
        "model": "snowflake-arctic-embed",
        "dimensions": 1024
    },
    "bge-m3": {
        "provider": "ollama",
        "model": "bge-m3",
        "dimensions": 1024
    }
}

# llama.cpp GGUF model presets (user must download and specify path)
LLAMACPP_PRESETS = {
    "nomic-embed-text-v1.5": {
        "provider": "llamacpp",
        "model": "nomic-embed-text-v1.5.Q8_0.gguf",
        "dimensions": 768,
        "url": "https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF"
    },
    "bge-small-en-v1.5": {
        "provider": "llamacpp",
        "model": "bge-small-en-v1.5.Q8_0.gguf",
        "dimensions": 384,
        "url": "https://huggingface.co/second-state/bge-small-en-v1.5-GGUF"
    },
    "all-MiniLM-L6-v2": {
        "provider": "llamacpp",
        "model": "all-MiniLM-L6-v2.Q8_0.gguf",
        "dimensions": 384,
        "url": "https://huggingface.co/second-state/all-MiniLM-L6-v2-GGUF"
    },
    "bge-base-en-v1.5": {
        "provider": "llamacpp",
        "model": "bge-base-en-v1.5.Q8_0.gguf",
        "dimensions": 768,
        "url": "https://huggingface.co/second-state/bge-base-en-v1.5-GGUF"
    }
}


def get_config() -> dict:
    """Load configuration from file and environment variables."""
    config = DEFAULT_CONFIG.copy()
    
    # Load from config file
    config_path = Path(".branch-flow/config.json")
    if config_path.exists():
        with open(config_path) as f:
            file_config = json.load(f)
            if "embedding" in file_config:
                config["embedding"].update(file_config["embedding"])
            if "index" in file_config:
                config["index"].update(file_config["index"])
    
    # Environment variable overrides
    env_mappings = {
        "BF_EMBEDDING_PROVIDER": ("embedding", "provider"),
        "BF_EMBEDDING_MODEL": ("embedding", "model"),
        "BF_EMBEDDING_DIMENSIONS": ("embedding", "dimensions", int),
        "BF_OLLAMA_URL": ("embedding", "ollama_url"),
        "BF_CHUNK_SIZE": ("embedding", "chunk_size", int),
    }
    
    for env_var, mapping in env_mappings.items():
        value = os.environ.get(env_var)
        if value:
            section, key = mapping[0], mapping[1]
            converter = mapping[2] if len(mapping) > 2 else str
            config[section][key] = converter(value)
    
    # Apply model preset if specified
    model = config["embedding"]["model"]
    if model in MODEL_PRESETS:
        preset = MODEL_PRESETS[model]
        config["embedding"]["provider"] = preset["provider"]
        config["embedding"]["dimensions"] = preset["dimensions"]
    
    return config


# =============================================================================
# Embedding Providers
# =============================================================================

def get_ollama_embedding(text: str, config: dict) -> List[float]:
    """Get embedding from Ollama."""
    import urllib.request
    import urllib.error
    
    url = f"{config['embedding']['ollama_url']}/api/embeddings"
    data = json.dumps({
        "model": config["embedding"]["model"],
        "prompt": text
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result["embedding"]
    except urllib.error.URLError as e:
        print(f"Error connecting to Ollama: {e}", file=sys.stderr)
        print(f"Make sure Ollama is running: ollama serve", file=sys.stderr)
        sys.exit(1)


def get_llamacpp_embedding(text: str, config: dict) -> List[float]:
    """Get embedding from llama.cpp server."""
    import urllib.request
    import urllib.error
    
    url = f"{config['embedding'].get('llamacpp_url', 'http://localhost:8080')}/embedding"
    data = json.dumps({
        "content": text
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            # llama.cpp returns {"embedding": [...]} or {"data": [{"embedding": [...]}]}
            if "embedding" in result:
                return result["embedding"]
            elif "data" in result and len(result["data"]) > 0:
                return result["data"][0]["embedding"]
            else:
                raise ValueError(f"Unexpected response format: {result.keys()}")
    except urllib.error.URLError as e:
        print(f"Error connecting to llama.cpp server: {e}", file=sys.stderr)
        print(f"Make sure llama-server is running with --embedding flag:", file=sys.stderr)
        print(f"  llama-server -m <model.gguf> --embedding --port 8080", file=sys.stderr)
        sys.exit(1)


def get_embedding(text: str, config: dict) -> List[float]:
    """Get embedding using configured provider."""
    provider = config["embedding"]["provider"]
    
    if provider == "ollama":
        return get_ollama_embedding(text, config)
    elif provider == "llamacpp":
        return get_llamacpp_embedding(text, config)
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'ollama' or 'llamacpp'.")


def ensure_model_available(config: dict) -> bool:
    """Check if the embedding model is available, pull if needed."""
    provider = config["embedding"]["provider"]
    
    if provider == "llamacpp":
        # For llama.cpp, check if server is running
        return ensure_llamacpp_server(config)
    elif provider == "ollama":
        return ensure_ollama_model(config)
    else:
        print(f"Unknown provider: {provider}", file=sys.stderr)
        return False


def ensure_llamacpp_server(config: dict) -> bool:
    """Check if llama.cpp server is running with embedding support."""
    import urllib.request
    import urllib.error
    
    url = config["embedding"].get("llamacpp_url", "http://localhost:8080")
    
    try:
        # Try to hit the health endpoint or embedding endpoint
        req = urllib.request.Request(f"{url}/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            return True
    except urllib.error.URLError:
        pass
    
    # Try a simple embedding request to verify
    try:
        test_url = f"{url}/embedding"
        data = json.dumps({"content": "test"}).encode('utf-8')
        req = urllib.request.Request(test_url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return True
    except urllib.error.URLError as e:
        print(f"⚠️  llama.cpp server not available at {url}", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"Start the server with:", file=sys.stderr)
        print(f"  llama-server -m <model.gguf> --embedding --port 8080", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"Example:", file=sys.stderr)
        print(f"  llama-server -m nomic-embed-text-v1.5.Q8_0.gguf --embedding --port 8080", file=sys.stderr)
        return False


def ensure_ollama_model(config: dict) -> bool:
    """Check if Ollama model is available, pull if needed."""
    model = config["embedding"]["model"]
    
    # Check if model exists
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if model in result.stdout:
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("Ollama not found. Please install: https://ollama.ai", file=sys.stderr)
        return False
    
    # Pull the model
    print(f"Pulling embedding model: {model}")
    try:
        subprocess.run(["ollama", "pull", model], check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to pull model: {model}", file=sys.stderr)
        return False


# =============================================================================
# Text Chunking
# =============================================================================

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict]:
    """Split text into overlapping chunks with metadata."""
    chunks = []
    lines = text.split('\n')
    current_chunk = []
    current_size = 0
    start_line = 0
    
    for i, line in enumerate(lines):
        line_size = len(line) + 1  # +1 for newline
        
        if current_size + line_size > chunk_size and current_chunk:
            chunk_text = '\n'.join(current_chunk)
            chunks.append({
                "text": chunk_text,
                "start_line": start_line,
                "end_line": i - 1
            })
            
            # Calculate overlap
            overlap_lines = []
            overlap_size = 0
            for j in range(len(current_chunk) - 1, -1, -1):
                if overlap_size + len(current_chunk[j]) > overlap:
                    break
                overlap_lines.insert(0, current_chunk[j])
                overlap_size += len(current_chunk[j]) + 1
            
            current_chunk = overlap_lines
            current_size = overlap_size
            start_line = i - len(overlap_lines)
        
        current_chunk.append(line)
        current_size += line_size
    
    if current_chunk:
        chunks.append({
            "text": '\n'.join(current_chunk),
            "start_line": start_line,
            "end_line": len(lines) - 1
        })
    
    return chunks


# =============================================================================
# Database / Index
# =============================================================================

def init_database(db_path: Path, dimensions: int):
    """Initialize SQLite database for vector storage."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            start_line INTEGER,
            end_line INTEGER,
            file_hash TEXT NOT NULL,
            doc_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(file_path, chunk_index)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            doc_id INTEGER PRIMARY KEY,
            embedding BLOB NOT NULL,
            FOREIGN KEY (doc_id) REFERENCES documents(id)
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_file_path ON documents(file_path)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_doc_type ON documents(doc_type)
    """)
    
    conn.commit()
    return conn


def file_hash(path: Path) -> str:
    """Calculate file hash for change detection."""
    return hashlib.md5(path.read_bytes()).hexdigest()


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def serialize_embedding(embedding: List[float]) -> bytes:
    """Serialize embedding to bytes for storage."""
    import struct
    return struct.pack(f'{len(embedding)}f', *embedding)


def deserialize_embedding(data: bytes) -> List[float]:
    """Deserialize embedding from bytes."""
    import struct
    count = len(data) // 4
    return list(struct.unpack(f'{count}f', data))


# =============================================================================
# Indexing
# =============================================================================

def should_index_file(path: Path, config: dict) -> bool:
    """Check if file should be indexed."""
    # Check extension
    if path.suffix not in config["index"]["include_extensions"]:
        return False
    
    # Check excluded filenames
    exclude_files = config["index"].get("exclude_files", [])
    if path.name in exclude_files:
        return False
    
    # Check exclude patterns
    path_str = str(path)
    for pattern in config["index"]["exclude_patterns"]:
        if pattern in path_str:
            return False
    
    # Check file size
    try:
        size_kb = path.stat().st_size / 1024
        if size_kb > config["index"]["max_file_size_kb"]:
            return False
    except OSError:
        return False
    
    return True


def get_files_to_index(config: dict) -> List[Tuple[Path, str]]:
    """Get list of files to index with their types."""
    files = []
    root = Path(".")
    
    # Index codebase
    if config["index"]["index_codebase"]:
        for path in root.rglob("*"):
            if path.is_file() and should_index_file(path, config):
                files.append((path, "code"))
    
    # Index memory
    if config["index"]["index_memory"]:
        memory_dir = root / ".branch-flow" / "memory"
        if memory_dir.exists():
            for path in memory_dir.glob("*.md"):
                files.append((path, "memory"))
    
    # Index specs
    if config["index"]["index_specs"]:
        specs_dir = root / ".branch-flow" / "specs"
        if specs_dir.exists():
            for path in specs_dir.glob("*.md"):
                files.append((path, "spec"))
        
        plans_dir = root / ".branch-flow" / "plans"
        if plans_dir.exists():
            for path in plans_dir.glob("*.md"):
                files.append((path, "plan"))
    
    return files


def index_file(conn: sqlite3.Connection, path: Path, doc_type: str, config: dict):
    """Index a single file."""
    cursor = conn.cursor()
    
    # Check if file has changed
    current_hash = file_hash(path)
    cursor.execute(
        "SELECT file_hash FROM documents WHERE file_path = ? LIMIT 1",
        (str(path),)
    )
    row = cursor.fetchone()
    
    if row and row[0] == current_hash:
        return False  # No change
    
    # Remove old entries
    cursor.execute(
        "DELETE FROM embeddings WHERE doc_id IN (SELECT id FROM documents WHERE file_path = ?)",
        (str(path),)
    )
    cursor.execute("DELETE FROM documents WHERE file_path = ?", (str(path),))
    
    # Read and chunk file
    try:
        content = path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"  Error reading {path}: {e}", file=sys.stderr)
        return False
    
    chunks = chunk_text(
        content,
        config["embedding"]["chunk_size"],
        config["embedding"]["chunk_overlap"]
    )
    
    # Index each chunk
    for i, chunk in enumerate(chunks):
        # Insert document
        cursor.execute("""
            INSERT INTO documents (file_path, chunk_index, content, start_line, end_line, file_hash, doc_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (str(path), i, chunk["text"], chunk["start_line"], chunk["end_line"], current_hash, doc_type))
        
        doc_id = cursor.lastrowid
        
        # Get and store embedding
        embedding = get_embedding(chunk["text"], config)
        cursor.execute(
            "INSERT INTO embeddings (doc_id, embedding) VALUES (?, ?)",
            (doc_id, serialize_embedding(embedding))
        )
    
    conn.commit()
    return True


def build_index(config: dict, verbose: bool = True):
    """Build or update the search index."""
    # Ensure index directory exists
    index_dir = Path(".branch-flow/index")
    index_dir.mkdir(parents=True, exist_ok=True)
    
    db_path = index_dir / "search.db"
    
    # Ensure model is available
    if not ensure_model_available(config):
        return False
    
    # Initialize database
    conn = init_database(db_path, config["embedding"]["dimensions"])
    
    # Get files to index
    files = get_files_to_index(config)
    
    if verbose:
        print(f"Indexing {len(files)} files...")
    
    indexed = 0
    errors = 0
    for path, doc_type in files:
        if verbose:
            print(f"  {path}", end="", flush=True)
        
        try:
            changed = index_file(conn, path, doc_type, config)
            
            if verbose:
                print(" ✓" if changed else " (unchanged)")
            
            if changed:
                indexed += 1
        except Exception as e:
            errors += 1
            if verbose:
                print(f" ✗ Error: {e}")
            # Continue with next file instead of stopping
            continue
    
    conn.close()
    
    if verbose:
        print(f"\n✅ Indexed {indexed} files ({len(files)} total)")
        if errors > 0:
            print(f"⚠️  {errors} files had errors (skipped)")
    
    return True


# =============================================================================
# Search
# =============================================================================

def search(query: str, config: dict, limit: int = 10, doc_type: Optional[str] = None) -> List[Dict]:
    """Search the index for relevant documents."""
    db_path = Path(".branch-flow/index/search.db")
    
    if not db_path.exists():
        print("Index not found. Run: /bf:index", file=sys.stderr)
        return []
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get query embedding
    query_embedding = get_embedding(query, config)
    
    # Get all embeddings
    if doc_type:
        cursor.execute("""
            SELECT d.id, d.file_path, d.content, d.start_line, d.end_line, d.doc_type, e.embedding
            FROM documents d
            JOIN embeddings e ON d.id = e.doc_id
            WHERE d.doc_type = ?
        """, (doc_type,))
    else:
        cursor.execute("""
            SELECT d.id, d.file_path, d.content, d.start_line, d.end_line, d.doc_type, e.embedding
            FROM documents d
            JOIN embeddings e ON d.id = e.doc_id
        """)
    
    results = []
    for row in cursor.fetchall():
        doc_id, file_path, content, start_line, end_line, dtype, embedding_blob = row
        embedding = deserialize_embedding(embedding_blob)
        similarity = cosine_similarity(query_embedding, embedding)
        
        results.append({
            "file_path": file_path,
            "content": content,
            "start_line": start_line,
            "end_line": end_line,
            "doc_type": dtype,
            "similarity": similarity
        })
    
    conn.close()
    
    # Sort by similarity and return top results
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:limit]


def find_similar(file_path: str, config: dict, limit: int = 10) -> List[Dict]:
    """Find files similar to the given file."""
    path = Path(file_path)
    
    if not path.exists():
        print(f"File not found: {file_path}", file=sys.stderr)
        return []
    
    content = path.read_text(encoding='utf-8', errors='ignore')
    
    # Use file content as query
    return search(content[:config["embedding"]["chunk_size"]], config, limit + 1)


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Branch Flow Semantic Search")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Index command
    index_parser = subparsers.add_parser("index", help="Build or update search index")
    index_parser.add_argument("-q", "--quiet", action="store_true", help="Quiet output")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search the index")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("-n", "--limit", type=int, default=10, help="Number of results")
    search_parser.add_argument("-t", "--type", choices=["code", "memory", "spec", "plan"], help="Filter by type")
    search_parser.add_argument("--json", action="store_true", help="JSON output")
    
    # Similar command
    similar_parser = subparsers.add_parser("similar", help="Find similar files")
    similar_parser.add_argument("file", help="File to find similar to")
    similar_parser.add_argument("-n", "--limit", type=int, default=10, help="Number of results")
    similar_parser.add_argument("--json", action="store_true", help="JSON output")
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Show or update configuration")
    config_parser.add_argument("--set-model", help="Set embedding model")
    config_parser.add_argument("--list-models", action="store_true", help="List available models")
    
    args = parser.parse_args()
    config = get_config()
    
    if args.command == "index":
        build_index(config, verbose=not args.quiet)
    
    elif args.command == "search":
        results = search(args.query, config, args.limit, args.type)
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            if not results:
                print("No results found.")
                return
            
            print(f"\n🔍 Search results for: {args.query}\n")
            for i, r in enumerate(results, 1):
                score = r["similarity"] * 100
                print(f"{i}. [{r['doc_type']}] {r['file_path']}:{r['start_line']}-{r['end_line']}")
                print(f"   Score: {score:.1f}%")
                preview = r["content"][:200].replace('\n', ' ')
                print(f"   {preview}...")
                print()
    
    elif args.command == "similar":
        results = find_similar(args.file, config, args.limit)
        
        # Filter out the source file itself
        results = [r for r in results if r["file_path"] != args.file]
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            if not results:
                print("No similar files found.")
                return
            
            print(f"\n📄 Files similar to: {args.file}\n")
            for i, r in enumerate(results, 1):
                score = r["similarity"] * 100
                print(f"{i}. [{r['doc_type']}] {r['file_path']}")
                print(f"   Similarity: {score:.1f}%")
                print()
    
    elif args.command == "config":
        if args.list_models:
            print("\n📋 Available embedding models:\n")
            for name, preset in MODEL_PRESETS.items():
                marker = "→" if name == config["embedding"]["model"] else " "
                print(f"  {marker} {name} ({preset['dimensions']} dimensions)")
            print(f"\nCurrent model: {config['embedding']['model']}")
            print("\nTo change: bf-search.py config --set-model <name>")
            print("Or set environment variable: BF_EMBEDDING_MODEL=<name>")
        
        elif args.set_model:
            config_path = Path(".branch-flow/config.json")
            if config_path.exists():
                with open(config_path) as f:
                    file_config = json.load(f)
            else:
                file_config = {}
            
            if "embedding" not in file_config:
                file_config["embedding"] = {}
            
            file_config["embedding"]["model"] = args.set_model
            
            if args.set_model in MODEL_PRESETS:
                file_config["embedding"]["dimensions"] = MODEL_PRESETS[args.set_model]["dimensions"]
            
            with open(config_path, "w") as f:
                json.dump(file_config, f, indent=2)
            
            print(f"✅ Model set to: {args.set_model}")
            print("Run '/bf:index' to rebuild the index with the new model.")
        
        else:
            print(json.dumps(config, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
