# token-utils

A comprehensive utility library for tokenization that allows you to use pre-downloaded tokenizers (like Hugging Face or Jina) for tokenizing, counting tokens, and chunking text.

## Features

- **Multiple Tokenizer Support**: Built-in support for Hugging Face and Jina tokenizers
- **Automatic Tokenizer Discovery**: Automatically finds tokenizers in common locations
- **Flexible Configuration**: Download tokenizers programmatically or from config files
- **Text Chunking**: Split text into chunks with configurable overlap
- **Token Counting**: Accurately count tokens in text
- **Environment Variable Configuration**: Customize tokenizer storage location

## Installation

Install the package via pip:

```bash
pip install token-utils
```

Or install from local source:

```bash
pip install .
```

For development installation with test dependencies:

```bash
pip install -e .[test]
```

## Quick Start

### Basic Tokenization

```python
from token_utils import TokenizationManager

# Initialize with a registered tokenizer name
manager = TokenizationManager("hf")  # or "jina"

# Or use a custom downloaded tokenizer by providing the path to the tokenizer directory
# The path should point to the directory containing tokenizer.json, config.json, vocab.json, etc.
manager = TokenizationManager("qwen", model_path="/path/to/downloaded/qwen/")

# Tokenize text
tokens = manager.tokenize("Hello world")
print(tokens)  # Output: [15496, 995]

# Count tokens
count = manager.count_tokens("Hello world")
print(count)  # Output: 2
```

### Text Chunking

```python
from token_utils import TokenizationManager

manager = TokenizationManager("hf")

# Chunk text into pieces of 50 tokens with 10 token overlap
chunks = manager.chunk_text("Your long text here...", chunk_size=50, overlap=10)
print(chunks)  # Output: list of text chunks
```

### Finding Available Tokenizers

```python
from token_utils import find_available_tokenizers

# Discover what tokenizers are available on your system
available = find_available_tokenizers()
print("Found tokenizers:", available)
# Output: {'qwen': '/home/user/models/qwen', 'bert': '/home/user/.cache/huggingface/tokenizers/bert'}
```

## Core Components

### TokenizationManager

Main interface for tokenization operations:

```python
TokenizationManager(tokenizer_name: str, model_path: str = None)
```

Parameters:
- `tokenizer_name`: Name of the tokenizer ("hf", "jina", or custom name)
- `model_path`: Optional explicit path to tokenizer directory (should contain tokenizer.json, config.json, vocab.json, etc.)

Methods:
- `tokenize(text: str) -> list[int]`: Convert text to token IDs
- `count_tokens(text: str) -> int`: Count tokens in text
- `chunk_text(text: str, chunk_size: int, overlap: int = 0) -> list[str]`: Split text into chunks

### TokenizerDownloader

Handles downloading and managing tokenizer files:

```python
TokenizerDownloader()
```

Methods:
- `set_config(config: dict)`: Set tokenizer download configurations
- `download_tokenizer(name: str) -> str`: Download a specific tokenizer
- `download_from_file(file_path: str)`: Download tokenizers from config file
- `find_tokenizers_on_system(search_paths: list) -> dict`: Find tokenizers on filesystem
- `auto_detect_tokenizer(name: str) -> str`: Auto-detect tokenizer location
- `get_tokenizer_path(name: str) -> str`: Get path for tokenizer (downloads if needed)

## Available Tokenizers

The package includes two tokenizer implementations by default:

1. **HFTokenizer**: For Hugging Face tokenizers (can download automatically)
2. **JinaTokenizer**: Specifically for Jina tokenizers (extends HFTokenizer, can download automatically)

Both tokenizers extend the base `BaseTokenizer` abstract class.

## Setting Up Tokenizers

You can either:

1. **Manual setup**: Download tokenizer files and set `TOKENIZER_DIR` environment variable
2. **Automatic download**: Configure URLs and let the library download them

### Manual Setup

Download your tokenizer files and place them in a directory, then set:

```bash
export TOKENIZER_DIR=/path/to/tokenizers
```

Example directory structure:
```
/path/to/tokenizers/
├── hf/
│   ├── config.json
│   ├── tokenizer.json
│   ├── tokenizer_config.json
│   ├── vocab.json
│   └── special_tokens_map.json
└── jina/
    ├── config.json
    ├── tokenizer.json
    ├── tokenizer_config.json
    ├── vocab.json
    └── special_tokens_map.json
```

### Automatic Download

For built-in tokenizers like "jina", URLs are pre-configured. For custom tokenizers, set URLs programmatically:

```python
from token_utils import TokenizerDownloader

downloader = TokenizerDownloader()
downloader.set_config({"my_model": "https://huggingface.co/user/model/resolve/main/"})
# Then use TokenizationManager("my_model") - it will download automatically
```

**Note**: URLs should point to complete tokenizer directories or downloadable archives. Single files like `tokenizer.json` may not be sufficient for all tokenizers.

Downloaded tokenizers are stored in the `TOKENIZER_DIR` directory (defaults to `/app/tokenizers`).

### Using Already Downloaded Tokenizers

If you have already downloaded a tokenizer but don't know the exact path, the library can help you find and use it:

1. **Auto-detection**: The library will automatically search for tokenizers in common locations:
   ```python
   from token_utils import TokenizationManager

   # Will automatically find and use the tokenizer
   manager = TokenizationManager("qwen")
   ```

2. **Find available tokenizers**: Discover what tokenizers are available on your system:
   ```python
   from token_utils import find_available_tokenizers

   available = find_available_tokenizers()
   print("Found tokenizers:", available)
   ```

3. **Specify path directly** (if auto-detection doesn't work):
    ```python
    manager = TokenizationManager("qwen", model_path="/path/to/downloaded/qwen/")
    ```

4. **Set TOKENIZER_DIR**: For organized storage:
   ```bash
   export TOKENIZER_DIR=/path/to/my/tokenizers
   # Place Qwen tokenizer in /path/to/my/tokenizers/qwen/
   ```
   Then use:
   ```python
   manager = TokenizationManager("qwen")
   ```

The auto-detection searches in these locations by default:
- `$TOKENIZER_DIR` (your configured tokenizer directory)
- `~/.cache/huggingface/tokenizers` (Hugging Face cache)
- `~/models` and `~/tokenizers` (common user directories)
- `/opt/tokenizers` and `/usr/local/tokenizers` (system directories)

## Configuration File Format

Config files can be either `.txt` or `.json` format:

### TXT Format (`tokenizers.txt`):
```
my_tokenizer = https://example.com/tokenizer.zip
another_tokenizer = https://huggingface.co/user/model/resolve/main/tokenizer.json
```

### JSON Format (`tokenizers.json`):
```json
{
  "my_tokenizer": "https://example.com/tokenizer.zip",
  "another_tokenizer": "https://huggingface.co/user/model/resolve/main/tokenizer.json"
}
```

## API Reference

### TokenizationManager

```python
class TokenizationManager:
    def __init__(self, tokenizer_name: str, model_path: str = None)
    def tokenize(self, text: str) -> list[int]
    def count_tokens(self, text: str) -> int
    def chunk_text(self, text: str, chunk_size: int, overlap: int = 0) -> list[str]
```

### TokenizerDownloader

```python
class TokenizerDownloader:
    def __init__(self)
    def set_config(self, config: dict) -> None
    def download_tokenizer(self, name: str) -> str
    def download_from_file(self, file_path: str) -> None
    def find_tokenizers_on_system(self, search_paths: list = None) -> dict
    def auto_detect_tokenizer(self, name: str) -> str
    def get_tokenizer_path(self, name: str) -> str
```

### Utility Functions

```python
def find_available_tokenizers(search_paths: list = None) -> dict
```

## Requirements

- Python >= 3.10
- transformers >= 4.0.0
- requests >= 2.25.0

## Development and Testing

### Running Tests

Install test dependencies:
```bash
pip install -e .[test]
```

Run the test suite:
```bash
pytest tests/
```

### Test Structure

The test suite includes:
- **Unit tests** for individual components (downloader, manager, etc.)
- **Integration tests** with mock tokenizers
- **Configuration tests** for loading settings from files
- **Auto-detection tests** for finding tokenizers on the system

### Creating Test Tokenizers

For development and testing, you can create mock tokenizers:
```bash
python tests/create_mock_tokenizers.py
```

This creates minimal tokenizer configurations for testing purposes.

### Testing with Real Tokenizers

The package has been tested with real tokenizers downloaded from Hugging Face:
```bash
# Download and test GPT-2 tokenizer
python -c "
import requests
from pathlib import Path
import os

# Download GPT-2 tokenizer files
tokenizer_dir = Path('/tmp/real_gpt2')
tokenizer_dir.mkdir(exist_ok=True)

files = ['tokenizer.json', 'vocab.json', 'merges.txt', 'tokenizer_config.json']
base_url = 'https://huggingface.co/gpt2/resolve/main/'

for file in files:
    response = requests.get(base_url + file)
    with open(tokenizer_dir / file, 'wb') as f:
        f.write(response.content)

# Use with token-utils
from token_utils import TokenizationManager
manager = TokenizationManager('gpt2', model_path=str(tokenizer_dir))
tokens = manager.tokenize('Hello world!')
print(f'Tokens: {tokens}')
"
```

The package successfully works with real Hugging Face tokenizers including GPT-2, DistilBERT, and others.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request