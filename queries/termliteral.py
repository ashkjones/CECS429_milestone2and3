from indexing.postings import Posting
from text import TokenProcessor
from text.notokenprocessor import NoTokenProcessor
from .querycomponent import QueryComponent

class TermLiteral(QueryComponent):
    """
    A TermLiteral represents a single term in a subquery.
    """
    tokenizer : TokenProcessor = NoTokenProcessor()

    def __init__(self, term : str):
        QueryComponent.__init__(self)
        self.term = term


    def get_postings(self, index) -> list[Posting]:
        # other booleans don't need postings
        print("blooop")
        return index.get_np_postings(self.tokenizer.process_token(self.term)[-1])


    def __str__(self) -> str:
        return self.term