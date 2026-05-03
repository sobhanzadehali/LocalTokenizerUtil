class TokenizerLoadingError(Exception):
    """Raised when the tokenizer cannot be loaded."""

    def __init__(self, message: str = "failed to load tokenizer()"):
        self.message = message
        super().__init__(self.message)


class FileNotFoundError(Exception):
    """Raised when a file is not found."""

    def __init__(self, message: str = "file not found"):
        self.message = message
        super().__init__(self.message)
