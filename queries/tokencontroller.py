from text import TokenProcessor
from queries import SpecialQuery, TermLiteral, PhraseLiteral

"""TokenController sets the tokenizer for certain query classes"""
class TokenController():

    # i think this makes it a singleton class. Idk how design patterns work in python
    def __new__(cls, tokenizer):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TokenController, cls).__new__(cls)
        return cls.instance

    def __init__(self, tokenizer : TokenProcessor):
        self._tokenizer = tokenizer
        SpecialQuery.tokenizer = tokenizer
        TermLiteral.tokenizer = tokenizer
        PhraseLiteral.tokenizer = tokenizer

    @property
    def tokenizer(self, tokenizer : TokenProcessor):
        self._tokenizer = tokenizer
        SpecialQuery.tokenizer = tokenizer
        TermLiteral.tokenizer = tokenizer
        PhraseLiteral.tokenizer = tokenizer

    

