from abc import ABC, abstractmethod

from transformers import AutoTokenizer


class BaseTokenizer(ABC):
    """
    Abstract base class for tokenizers. all tokenizers should inherit from this class.
    """

    @abstractmethod
    def encode(self, text: str) -> list[int]:
        pass

    @abstractmethod
    def decode(self, tokens: list[int]) -> str:
        pass


