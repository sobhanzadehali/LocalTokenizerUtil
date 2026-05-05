#!/usr/bin/env python3
"""
Script to download real tokenizers for testing.
This script downloads some lightweight tokenizers for use in tests.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from token_utils import TokenizerDownloader


def download_test_tokenizers():
    """Download tokenizers for testing."""
    downloader = TokenizerDownloader()

    # Set up test tokenizer directory
    test_tokenizers_dir = Path(__file__).parent / "test_tokenizers"
    test_tokenizers_dir.mkdir(exist_ok=True)

    # Set TOKENIZER_DIR to test directory
    os.environ["TOKENIZER_DIR"] = str(test_tokenizers_dir)

    # Also configure the downloader to use this directory
    downloader.base_dir = test_tokenizers_dir

    # Configure URLs for lightweight tokenizers
    test_configs = {
        "bert-tiny": "https://huggingface.co/prajjwal1/bert-tiny/resolve/main/tokenizer.json",
        "distilbert-base-uncased": "https://huggingface.co/distilbert/distilbert-base-uncased/resolve/main/tokenizer.json",
    }

    print("Downloading test tokenizers...")

    for name, url in test_configs.items():
        try:
            print(f"Downloading {name}...")
            path = downloader.download_tokenizer(name, url)
            print(f"✓ Downloaded {name} to {path}")
        except Exception as e:
            print(f"✗ Failed to download {name}: {e}")

    print("\nTest tokenizers setup complete!")
    print(f"Tokenizers downloaded to: {test_tokenizers_dir}")


if __name__ == "__main__":
    download_test_tokenizers()