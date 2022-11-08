from abc import ABC, abstractmethod
from typing import Iterable
from .postings import Posting

class Index(ABC):
    """An Index can retrieve postings for a term from a data structure associating terms and the documents
    that contain them."""


    def get_p_postings(self, term : str) -> Iterable[Posting]:
        """Retrieves a sequence of Postings of documents that contain the given term including position info."""
        pass

    def get_np_postings(self, term : str) -> Iterable[Posting]:
        """Retrieves a sequence of Postings of documents that contain the given term without position."""
        pass

    def vocabulary(self) -> list[str]:
        """A (sorted) list of all terms in the index vocabulary."""
        pass