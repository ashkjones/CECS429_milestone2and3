from typing import List


class Posting:
    """A Posting encapsulates a document ID and term positions associated with a search query component."""

    def __init__(self, doc_id : int, pos : List[int] = []):
        self.doc_id = doc_id
        self.positions = [s for s in pos]

    def add_term(self, pos : int):
        self.positions.append(pos)
