import pytest
import os
import tempfile
from pathlib import Path
from token_utils import TokenizerDownloader, TokenizationManager


@pytest.fixture(scope="session")
def temp_tokenizer_dir():
    """Create a temporary directory for tokenizer testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set TOKENIZER_DIR to temp directory
        old_tokenizer_dir = os.environ.get("TOKENIZER_DIR")
        os.environ["TOKENIZER_DIR"] = temp_dir
        yield temp_dir
        # Restore original TOKENIZER_DIR
        if old_tokenizer_dir:
            os.environ["TOKENIZER_DIR"] = old_tokenizer_dir
        elif "TOKENIZER_DIR" in os.environ:
            del os.environ["TOKENIZER_DIR"]


@pytest.fixture(scope="session")
def mock_tokenizers(temp_tokenizer_dir):
    """Create mock tokenizers for testing."""
    # Import here to avoid circular imports
    from tests.create_mock_tokenizers import create_mock_tokenizer
    from pathlib import Path

    mock_tokenizers_dir = Path(temp_tokenizer_dir)

    # Create some mock tokenizers
    tokenizers_to_create = ["test_gpt2", "test_bert", "test_qwen"]

    created_paths = {}
    for name in tokenizers_to_create:
        try:
            path = create_mock_tokenizer(name, mock_tokenizers_dir)
            created_paths[name] = str(path)
        except Exception as e:
            print(f"Failed to create mock tokenizer {name}: {e}")
            continue

    return created_paths


@pytest.fixture
def tokenizer_downloader():
    """Provide a TokenizerDownloader instance."""
    return TokenizerDownloader()