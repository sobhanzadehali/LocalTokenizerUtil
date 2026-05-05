#!/usr/bin/env python3
"""
Example: Using token-utils with real tokenizers

This example demonstrates how to use the token-utils package
with real tokenizers, including downloading and using them.
"""

import os
from token_utils import TokenizationManager, TokenizerDownloader, find_available_tokenizers


def example_download_and_use():
    """Example of downloading and using a tokenizer."""
    print("=== Token Utils Example ===\n")

    # Initialize downloader
    downloader = TokenizerDownloader()

    # Configure a tokenizer to download
    # Note: This is an example URL - replace with real tokenizer URLs
    print("1. Configuring tokenizer download...")
    downloader.set_config({
        "example_tokenizer": "https://example.com/tokenizer.zip"
    })

    # In a real scenario, you would download:
    # path = downloader.download_tokenizer("example_tokenizer")
    # print(f"Downloaded to: {path}")

    print("2. Finding available tokenizers on system...")
    available = find_available_tokenizers()
    print(f"Found tokenizers: {list(available.keys())}")

    # Example of using a tokenizer (would work with real tokenizers)
    print("\n3. Example usage with a tokenizer:")
    print("""
    # If you have a tokenizer at /path/to/my/tokenizer:
    manager = TokenizationManager("my_tokenizer", model_path="/path/to/my/tokenizer")

    text = "Hello, world! This is a test."
    tokens = manager.tokenize(text)
    count = manager.count_tokens(text)
    chunks = manager.chunk_text(text, chunk_size=10, overlap=2)

    print(f"Text: {text}")
    print(f"Tokens: {tokens}")
    print(f"Token count: {count}")
    print(f"Chunks: {chunks}")
    """)

    print("4. Loading config from file:")
    print("""
    # Create a tokenizers.txt file with:
    # my_tokenizer = https://example.com/tokenizer.zip
    # another_tokenizer = https://huggingface.co/user/model/resolve/main/

    # Then load and download:
    downloader.download_from_file("tokenizers.txt")
    """)

    print("\n=== Example Complete ===")


def example_with_mock_tokenizer():
    """Example using the mock tokenizers created for testing."""
    print("\n=== Testing with Mock Tokenizers ===\n")

    # Set up path to test tokenizers
    test_dir = os.path.join(os.path.dirname(__file__), "tests", "test_tokenizers")
    if os.path.exists(test_dir):
        print(f"Found test tokenizers in: {test_dir}")
        available = find_available_tokenizers([test_dir])
        print(f"Available test tokenizers: {list(available.keys())}")

        # Try to use one (this will likely fail because they're mock files)
        if available:
            first_tokenizer = list(available.keys())[0]
            try:
                manager = TokenizationManager(first_tokenizer, model_path=available[first_tokenizer])
                print(f"Successfully loaded {first_tokenizer}")
            except Exception as e:
                print(f"Expected failure with mock tokenizer: {e}")
    else:
        print("Test tokenizers not found. Run 'python tests/create_mock_tokenizers.py' first.")


if __name__ == "__main__":
    example_download_and_use()
    example_with_mock_tokenizer()