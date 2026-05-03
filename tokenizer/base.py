from abc import ABC, abstractmethod


class BaseTokenizerFactory(ABC):
    @abstractmethod
    def get_tokenizer(self, name_or_path: str):
        pass
