import logging

from transformers import AutoTokenizer

from tokenizer.base import BaseTokenizer
from tokenizer.exceptions import TokenizerLoadingError

logger = logging.getLogger(__name__)


class HuggingFaceTokenizer(BaseTokenizer):
    def __init__(self, name_or_path: str):
        try:
            self._tokenizer = AutoTokenizer.from_pretrained(
                name_or_path,
                trust_remote_code=True,
                local_files_only=True,
            )
        except Exception as e:
            logger.error(f"Failed to load local files, falling back to remote: {e}")
            raise TokenizerLoadingError(
                f"failed to load tokenizer({name_or_path}): {e}"
            )

    def encode(self, text: str) -> list[int]:
        return self._tokenizer.encode(text, add_special_tokens=False)

    def decode(self, tokens: list[int]) -> str:
        return self._tokenizer.decode(tokens)
