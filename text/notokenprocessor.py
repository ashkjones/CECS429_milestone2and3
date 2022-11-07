from .tokenprocessor import TokenProcessor

# needed because TokenProcessor is abstract
class NoTokenProcessor(TokenProcessor):
    """A NoTokenProcessor does no processing of tokens."""

    def process_token(self, token : str) -> list[str]:
        """Token is the term."""
        return [token]