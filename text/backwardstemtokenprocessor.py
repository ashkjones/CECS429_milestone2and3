from .tokenprocessor import TokenProcessor
import nltk
from nltk.stem.snowball import SnowballStemmer
import re

class BackStemTokenProcessor(TokenProcessor):
    """A BackStemTokenProcessor is an attempt to replicate the token processing used in the
    executable file provided as an example."""
    _whitespace_re = re.compile(r"^\W+|\W+$") 
    _quote_re = re.compile(r"[\"\']")
    _stemmer = SnowballStemmer(language='english')

    def process_token(self, token : str) -> list[str]:
        
        if len(token) <= 0:
            return []
        token = re.sub(self._quote_re, "", token.lower())
        tokens = token.lower().split("-")
        if len(tokens) > 1:
            tokens.append(token.replace("-", ""))
        for i in range(len(tokens)):
            tokens[i] = re.sub(self._whitespace_re, "", tokens[i])
            tokens[i] = BackStemTokenProcessor._stemmer.stem(tokens[i])
        return tokens
        

