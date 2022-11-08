from .tokenprocessor import TokenProcessor
import re
from nltk.stem.snowball import SnowballStemmer

class StemmingTokenProcessor(TokenProcessor):
    """A StemmingTokenProcessor creates terms from tokens by removing all non-alphanumeric characters 
    at the beginning and end of a token, converting it to all lowercase, removing hyphens, breaking at
    hyphens and stemming it using Porter2."""
    # _whitespace_re = re.compile(r"^\W+|\W+$") 

    # all the quotes go away. I hate special chars
    _quote_re = re.compile(r"[\u0027\u0022\u2018\u2019\u0060\u00B4\u201B\u201C\u201D]+")

    
    # Snowball is the better porter2 package that doesn't give different values for "the"
    # and break my code
    _stemmer = SnowballStemmer(language='english')
    
    def process_token(self, token : str) -> list[str]:
        if len(token) < 0:
            return []
        # lets just get rid of quotes first because my code hates me
        token = re.sub(self._quote_re, "", token)
        token = token.lower()
        length = len(token)
        start = length
        end = -1
        for i in range(length):
            if token[i].isalnum():
                start = i
                break
        for i in range(length):
            if token[length-i-1].isalnum():
                end = length-i
                break
        if start == end: #its all chars
            return list()
        token = token[start:end]
        terms = token.split("-")
        if len(terms) > 1:
            terms.append(token.replace("-", ""))
        terms = [StemmingTokenProcessor._stemmer.stem(x) for x in terms]  
        return terms
        

