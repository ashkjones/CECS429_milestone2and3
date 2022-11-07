from .tokenprocessor import TokenProcessor
import re
import nltk
from nltk.stem.snowball import SnowballStemmer

class StemmingTokenProcessor(TokenProcessor):
    """A StemmingTokenProcessor creates terms from tokens by removing all non-alphanumeric characters 
    at the beginning and end of a token, converting it to all lowercase, removing hyphens, breaking at
    hyphens and stemming it using Porter2."""
    _whitespace_re = re.compile(r"^\W+|\W+$") 
    _quote_re = re.compile(r"[\"\']")
    # Snowball is the better porter2 package that doesn't give different values for "the"
    # and break my code
    _stemmer =SnowballStemmer(language='english')

    
    def process_token(self, token : str) -> list[str]:
        if len(token) < 0:
            return []
        token = re.sub(self._whitespace_re, "", token.lower())
        token = re.sub(self._quote_re, "", token)
        terms = token.split("-")
        if len(terms) > 1:
            terms.append(token.replace("-", ""))
        terms = [StemmingTokenProcessor._stemmer.stem(x) for x in terms]  
        return terms
        

