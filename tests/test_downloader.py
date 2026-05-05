import pytest
import tempfile
import os
from pathlib import Path
from token_utils import TokenizerDownloader


class TestDownloaderFunctionality:
    """Test downloader specific functionality."""

    def test_download_config_file_txt(self, tmp_path):
        """Test loading configuration from a text file."""
        downloader = TokenizerDownloader()

        # Create a config file
        config_file = tmp_path / "tokenizers.txt"
        config_file.write_text("""
# Comment line
bert_tokenizer = https://example.com/bert.zip
gpt2_tokenizer = https://example.com/gpt2.zip
        """)

        downloader.load_config_from_file(str(config_file))

        assert "bert_tokenizer" in downloader.config
        assert "gpt2_tokenizer" in downloader.config
        assert downloader.config["bert_tokenizer"] == "https://example.com/bert.zip"

    def test_download_config_file_json(self, tmp_path):
        """Test loading configuration from a JSON file."""
        downloader = TokenizerDownloader()

        # Create a JSON config file
        config_file = tmp_path / "tokenizers.json"
        config_file.write_text('{"bert": "https://example.com/bert.zip"}')

        downloader.load_config_from_file(str(config_file))

        assert "bert" in downloader.config
        assert downloader.config["bert"] == "https://example.com/bert.zip"

    def test_download_from_file_integration(self, tmp_path):
        """Test the download_from_file method."""
        downloader = TokenizerDownloader()

        # Create a config file with a fake URL
        config_file = tmp_path / "tokenizers.txt"
        config_file.write_text("fake_tokenizer = https://httpbin.org/status/404")

        # This should attempt to download and fail gracefully
        results = downloader.download_from_file(str(config_file))

        # Should return empty list since download failed
        assert isinstance(results, list)

    def test_filename_extraction(self):
        """Test filename extraction from URLs and headers."""
        downloader = TokenizerDownloader()

        # Mock response object
        class MockResponse:
            def __init__(self, headers=None):
                self.headers = headers or {}

        # Test URL-based filename
        url = "https://example.com/model.zip"
        response = MockResponse()
        filename = downloader._get_filename_from_response(response, url)
        assert filename == "model.zip"

        # Test content-disposition filename
        response_with_cd = MockResponse({"content-disposition": 'attachment; filename="custom_model.json"'})
        filename = downloader._get_filename_from_response(response_with_cd, url)
        assert filename == "custom_model.json"

    def test_extraction_detection(self, tmp_path):
        """Test detection of compressed files."""
        downloader = TokenizerDownloader()

        # Test regular file (should not be extracted)
        regular_file = tmp_path / "test.json"
        regular_file.write_text("fake json content")
        result = downloader._extract_if_compressed(regular_file, tmp_path)
        assert result is None
        assert regular_file.exists()  # File should still exist

        # Note: Testing actual zip/tar extraction would require creating valid archive files
        # For this test, we just verify that non-compressed files are left alone