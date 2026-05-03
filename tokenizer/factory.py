from .base import BaseTokenizerFactory
from .mixin import LocalTokenizerMixin


class TokenizerFactory(BaseTokenizerFactory, LocalTokenizerMixin):
    """
    get a tokenizer from a local path or name with `get_tokenizer` method
    """

    def get_tokenizer(self, name_or_path: str):

        self._setup_local_tokenizer(name_or_path)
        return self.tokenizer
