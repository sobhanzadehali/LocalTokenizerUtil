from pathlib import Path

from transformers import AutoConfig, AutoTokenizer


class LocalTokenizerMixin:
    def _setup_local_tokenizer(self, name_or_path: str):
        tokenizer_dir = name_or_path
        base_cache = Path("/tokenizer_cache")
        model_cache_path = base_cache / f"models--{tokenizer_dir.replace('/', '--')}"

        if not model_cache_path.exists():
            raise FileNotFoundError(f"Model cache not found: {model_cache_path}")

        snapshot_folder = None
        snapshot_path = model_cache_path / "snapshot"
        if snapshot_path.exists():
            for snap in snapshot_path.iterdir():
                if snap.is_dir():
                    snapshot_folder = snap
                    break

        if snapshot_folder is None:
            raise FileNotFoundError(f"Snapshot folder not found: {snapshot_folder}")

        required_files = ["tokenizer.json", "vocab.json", "config.json"]
        missing_files = [
            f for f in required_files if not (snapshot_folder / f).exists()
        ]
        if missing_files:
            raise FileNotFoundError(f"Missing files: {missing_files}")
        config_path = snapshot_folder / "config.json"
        config = None
        if config_path.exists():
            config = AutoConfig.from_pretrained(
                str(snapshot_folder), local_files_only=True
            )
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                str(snapshot_folder),
                local_files_only=True,
                cache_dir=str(base_cache),
                config=config,
            )
        except Exception:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    tokenizer_dir,
                    cache_dir=str(base_cache),
                )
            except Exception as inner_e:
                raise RuntimeError(f"Failed to load tokenizer: {inner_e}") from inner_e
