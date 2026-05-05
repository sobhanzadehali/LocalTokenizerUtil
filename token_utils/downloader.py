import os
import requests
import zipfile
import tarfile
import shutil
from typing import Optional, Dict
from pathlib import Path


class TokenizerDownloader:
    def __init__(self, config: Optional[Dict[str, str]] = None):
        self.config = config or self._load_default_config()
        self.base_dir = Path(os.getenv("TOKENIZER_DIR", "/app/tokenizers"))

    def _load_default_config(self) -> Dict[str, str]:
        """Load default tokenizer URLs. Can be overridden by user config."""
        return {
            "jina": "https://huggingface.co/jinaai/jina-embeddings-v2-base-en/resolve/main/tokenizer.json?download=true",
            # Add more defaults as needed
        }

    def load_config_from_file(self, file_path: str):
        """Load configuration from a text file or JSON file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")

        if path.suffix == '.json':
            import json
            with open(path, 'r') as f:
                self.config.update(json.load(f))
        else:
            # Assume txt file with format: name=url
            with open(path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            name, url = line.split('=', 1)
                            self.config[name.strip()] = url.strip()

    def download_tokenizer(self, name: str, url: Optional[str] = None) -> str:
        """Download tokenizer from URL and return the local path."""
        if url is None:
            if name not in self.config:
                raise ValueError(f"No URL configured for tokenizer '{name}'")
            url = self.config[name]

        # Create directory for the tokenizer
        tokenizer_dir = self.base_dir / name
        tokenizer_dir.mkdir(parents=True, exist_ok=True)

        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Determine filename from URL or content-disposition
        filename = self._get_filename_from_response(response, url)
        local_path = tokenizer_dir / filename

        # Download the file
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # If it's a compressed file, extract it
        extracted_path = self._extract_if_compressed(local_path, tokenizer_dir)

        return str(extracted_path or tokenizer_dir)

    def _get_filename_from_response(self, response: requests.Response, url: str) -> str:
        """Get filename from response headers or URL."""
        if 'content-disposition' in response.headers:
            content_disp = response.headers['content-disposition']
            if 'filename=' in content_disp:
                # More robust filename extraction
                import re
                filename_match = re.search(r'filename[^;=\n]*=(([\'"]).*?\2|[^;\n]*)', content_disp)
                if filename_match:
                    filename = filename_match.group(1).strip('"\'' '')
                    return filename

        # Fallback to URL basename
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return os.path.basename(parsed.path) or 'downloaded_tokenizer'

    def _extract_if_compressed(self, file_path: Path, extract_to: Path) -> Optional[Path]:
        """Extract compressed files and return the extracted directory."""
        if file_path.suffix == '.zip':
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Extract to a subdirectory to avoid cluttering
                extract_dir = extract_to / file_path.stem
                extract_dir.mkdir(exist_ok=True)
                zip_ref.extractall(extract_dir)
            file_path.unlink()  # Remove the zip file
            return extract_dir
        elif file_path.suffix in ['.tar.gz', '.tgz', '.tar']:
            with tarfile.open(file_path, 'r:*') as tar_ref:
                extract_dir = extract_to / file_path.stem
                extract_dir.mkdir(exist_ok=True)
                tar_ref.extractall(extract_dir)
            file_path.unlink()
            return extract_dir

        # Not compressed, return None
        return None

    def get_tokenizer_path(self, name: str) -> str:
        """Get the local path for a tokenizer, downloading if necessary."""
        tokenizer_dir = self.base_dir / name

        if not tokenizer_dir.exists() or not any(tokenizer_dir.iterdir()):
            # Directory doesn't exist or is empty, try to download
            try:
                return self.download_tokenizer(name)
            except Exception as e:
                raise RuntimeError(f"Failed to download tokenizer '{name}': {e}")

        return str(tokenizer_dir)

    def set_config(self, config: Dict[str, str]):
        """Set configuration for tokenizer URLs."""
        self.config.update(config)

    def download_from_file(self, file_path: str):
        """Download multiple tokenizers from a config file."""
        self.load_config_from_file(file_path)

        downloaded = []
        for name in self.config:
            try:
                path = self.download_tokenizer(name)
                downloaded.append((name, path))
                print(f"Downloaded {name} to {path}")
            except Exception as e:
                print(f"Failed to download {name}: {e}")

        return downloaded

    def find_tokenizers_on_system(self, search_paths: Optional[list] = None) -> Dict[str, str]:
        """Search for tokenizer directories on the system."""
        if search_paths is None:
            # Common locations to search
            search_paths = [
                self.base_dir,
                Path.home() / ".cache" / "huggingface" / "tokenizers",
                Path.home() / "models",
                Path.home() / "tokenizers",
                Path("/opt/tokenizers"),
                Path("/usr/local/tokenizers"),
            ]
        else:
            # Convert string paths to Path objects
            search_paths = [Path(p) for p in search_paths]

        found_tokenizers = {}

        def is_tokenizer_dir(path: Path) -> bool:
            """Check if a directory contains tokenizer files."""
            if not path.is_dir():
                return False

            # Look for common tokenizer files
            tokenizer_files = [
                "tokenizer.json",
                "tokenizer_config.json",
                "vocab.json",
                "vocab.txt",
                "merges.txt",
                "special_tokens_map.json"
            ]

            return any((path / file).exists() for file in tokenizer_files)

        for search_path in search_paths:
            if not search_path.exists():
                continue

            # Search in subdirectories
            for item in search_path.iterdir():
                if item.is_dir() and is_tokenizer_dir(item):
                    name = item.name.lower()
                    found_tokenizers[name] = str(item)

        return found_tokenizers

    def auto_detect_tokenizer(self, name: str) -> Optional[str]:
        """Try to find a tokenizer with the given name on the system."""
        found = self.find_tokenizers_on_system()

        # Exact match first
        if name in found:
            return found[name]

        # Fuzzy match (contains name)
        for found_name, path in found.items():
            if name in found_name or found_name in name:
                return path

        return None