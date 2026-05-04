# token-utils

A utility library for tokenization that allows you to use pre-downloaded tokenizers (like Hugging Face or Jina) for tokenizing and chunking text.

## Installation

You can install the package via pip:

```bash
pip install token-utils
```

Or from the local source:

```bash
pip install .
```

## Usage

### Basic Tokenization

```python
from token_utils import TokenizationManager

# Initialize the manager with a tokenizer name (must be registered)
manager = TokenizationManager("hf")  # or "jina"

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

## Available Tokenizers

The package includes two tokenizer implementations by default:

1. **HFTokenizer**: For Hugging Face tokenizers (requires local files)
2. **JinaTokenizer**: Specifically for Jina tokenizers (extends HFTokenizer)

To use a tokenizer, you must have the tokenizer files available locally and set the `TOKENIZER_DIR` environment variable to point to the directory containing your tokenizers.

### Setting up Tokenizers

1. Download your tokenizer files (from Hugging Face or Jina) and place them in a directory.
2. Set the environment variable `TOKENIZER_DIR` to the path of that directory.

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

Then set:
```bash
export TOKENIZER_DIR=/path/to/tokenizers
```

## Requirements

- Python >= 3.13
- transformers >= 5.7.0

## License

MIT