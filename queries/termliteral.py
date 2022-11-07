from indexing.postings import Posting
from text import TokenProcessor
from text.notokenprocessor import NoTokenProcessor
from .querycomponent import QueryComponent

class TermLiteral(QueryComponent):
    """
    A TermLiteral represents a single term in a subquery.
    """
    _tokenizer : TokenProcessor = NoTokenProcessor()

    @property
    def tokenizer(tokenizer : TokenProcessor):
        TermLiteral._tokenizer = tokenizer

    def __init__(self, term : str):
        QueryComponent.__init__(self)
        self.term = term

    def get_postings(self, index) -> list[Posting]:
        return index.get_postings(self._tokenizer.process_token(self.term)[-1])


    def __str__(self) -> str:
        return self.term