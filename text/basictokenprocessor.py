from .tokenprocessor import TokenProcessor
import re

class BasicTokenProcessor(TokenProcessor):
    """A BasicTokenProcessor creates terms from tokens by removing all non-alphanumeric characters 
    from the token, and converting it to all lowercase."""
    _whitespace_re = re.compile(r"\W+")
    
    def process_token(self, token : str) -> list[str]:
        return [re.sub(self._whitespace_re, "", token).lower()]
