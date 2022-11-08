from bisect import bisect_left
from decimal import InvalidOperation
from pydoc import doc
from typing import Iterable
from .postings import Posting
from .index import Index
from .termfreqposting import TermFreqPosting


class PosInvertedIndex(Index):
    """Implements an Index using a term-document matrix. Requires knowing the full corpus
    vocabulary and number of documents prior to construction."""

    def __init__(self):
        """Constructs an empty index using the given vocabulary and corpus size."""
        self._matrix : dict = dict()
        

    def add_term(self, term : str, doc_id : int, pos : int):
        """Records that the given term occurred at a given position in the given document ID."""
        if term in self._matrix: 
            if doc_id == self._matrix[term][-1].doc_id:
                self._matrix[term][-1].positions.append(pos)
            else:
                self._matrix[term].append(Posting(doc_id, [pos]))
        else:
            self._matrix[term] = [Posting(doc_id, [pos])]
        

    def get_p_postings(self, term : str) -> Iterable[Posting]:
        """Returns a list of Postings for all documents that contain the given term."""
        if term in self._matrix:
            return self._matrix[term]
        else:
            return list()

    def get_np_postings(self, term : str) -> Iterable[Posting]:
        """Returns a list of Postings for all documents that contain the given term."""

        # seems silly but here we are.
        if term in self._matrix:
            postings_list = []
            for post in self._matrix[term]:
                postings_list.append(TermFreqPosting(post.doc_id, len(post.positions)))
        else:
            return list()

    
    def vocabulary(self) -> Iterable[str]:
        return sorted(list(self._matrix.keys()))