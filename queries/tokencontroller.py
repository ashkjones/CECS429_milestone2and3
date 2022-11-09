from text import TokenProcessor
from queries import SpecialQuery, TermLiteral, PhraseLiteral
from queries.rankedqueryparser import RankedQueryParser

"""TokenController sets the tokenizer for certain query classes"""
class TokenController():

    def __init__(self, tokenizer : TokenProcessor):
        self._tokenizer = tokenizer
        SpecialQuery.tokenizer = tokenizer
        TermLiteral.tokenizer = tokenizer
        PhraseLiteral.tokenizer = tokenizer
        RankedQueryParser.tokenizer = tokenizer

    @property
    def tokenizer(self):
        return self._tokenizer

    @tokenizer.setter
    def tokenizer(self, tokenizer : TokenProcessor):
        self._tokenizer = tokenizer
        SpecialQuery.tokenizer = tokenizer
        TermLiteral.tokenizer = tokenizer
        PhraseLiteral.tokenizer = tokenizer
        RankedQueryParser.tokenizer = tokenizer

    

