#!/usr/bin/env python3
"""
Script to create mock tokenizers for testing.
Since downloading real tokenizers can be complex, this creates minimal mock tokenizers.
"""

import json
import os
from pathlib import Path


def create_mock_tokenizer(name: str, base_dir: Path):
    """Create a minimal mock tokenizer for testing."""
    tokenizer_dir = base_dir / name
    tokenizer_dir.mkdir(exist_ok=True)

    # Create minimal tokenizer.json (simplified BPE-like tokenizer)
    tokenizer_config = {
        "model": {
            "type": "BPE",
            "vocab_size": 1000,
            "unk_token": "<unk>",
            "bos_token": "<s>",
            "eos_token": "</s>",
            "pad_token": "<pad>"
        },
        "pre_tokenizer": {
            "type": "Whitespace"
        },
        "normalizer": {
            "type": "NFC"
        }
    }

    with open(tokenizer_dir / "tokenizer.json", "w") as f:
        json.dump(tokenizer_config, f, indent=2)

    # Create tokenizer_config.json
    with open(tokenizer_dir / "tokenizer_config.json", "w") as f:
        json.dump({
            "model_type": "gpt2",
            "unk_token": "<unk>",
            "bos_token": "<s>",
            "eos_token": "</s>",
            "pad_token": "<pad>"
        }, f, indent=2)

    # Create a minimal vocab file
    with open(tokenizer_dir / "vocab.json", "w") as f:
        vocab = {f"token_{i}": i for i in range(1000)}
        vocab.update({
            "<unk>": 0,
            "<s>": 1,
            "</s>": 2,
            "<pad>": 3,
            "hello": 4,
            "world": 5,
            "!": 6
        })
        json.dump(vocab, f)

    # Create merges.txt for BPE
    with open(tokenizer_dir / "merges.txt", "w") as f:
        f.write("# BPE merges\n")
        f.write("h e\n")
        f.write("l l\n")
        f.write("o r\n")
        f.write("w o\n")

    return tokenizer_dir


def create_test_tokenizers():
    """Create test tokenizers for the test suite."""
    test_tokenizers_dir = Path(__file__).parent / "test_tokenizers"
    test_tokenizers_dir.mkdir(exist_ok=True)

    # Set TOKENIZER_DIR to test directory
    os.environ["TOKENIZER_DIR"] = str(test_tokenizers_dir)

    # Create mock tokenizers
    tokenizers = ["mock_gpt2", "mock_bert", "qwen_mock"]

    created = {}
    for name in tokenizers:
        try:
            path = create_mock_tokenizer(name, test_tokenizers_dir)
            created[name] = str(path)
            print(f"✓ Created mock tokenizer {name} at {path}")
        except Exception as e:
            print(f"✗ Failed to create {name}: {e}")

    print(f"\nMock tokenizers created in: {test_tokenizers_dir}")
    print(f"Set TOKENIZER_DIR={test_tokenizers_dir}")

    return created


if __name__ == "__main__":
    create_test_tokenizers()