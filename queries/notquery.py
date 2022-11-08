from .querycomponent import QueryComponent
from indexing import Index, Posting

class NotQuery(QueryComponent):

    def __init__(self, component):
        QueryComponent.__init__(self, False)
        self.component = component

    def get_postings(self, index : Index) -> list[Posting]:
        return self.component.get_np_postings(index)

    def __str__(self):
        return " - ".join(map(str, self.components))