from bisect import bisect_left
from decimal import InvalidOperation
from pydoc import doc
from typing import Iterable
from .postings import Posting
from .index import Index


class InvertedIndex(Index):
    """Implements an Index using a term-document matrix. Requires knowing the full corpus
    vocabulary and number of documents prior to construction."""

    def __init__(self):
        """Constructs an empty index using the given vocabulary and corpus size."""
        self._matrix : dict = dict()

    def add_term(self, term : str, doc_id : int, pos : int):
        """Records that the given term occurred in the given document ID."""
        if term in self._matrix: 
            if doc_id != self._matrix[term][-1]:
                self._matrix[term].append(doc_id)
        else:
            self._matrix[term] = [doc_id]
        

    def get_postings(self, term : str) -> Iterable[Posting]:
        """Returns a list of Postings for all documents that contain the given term."""
        if term in self._matrix:
            postings_list = []
            for id in self._matrix[term]:
                postings_list.append(Posting(id))
            return postings_list
        else:
            return list()

    
    def vocabulary(self) -> Iterable[str]:
        return self._matrix.keys().sort()