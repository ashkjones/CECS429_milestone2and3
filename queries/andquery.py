from . import OrQuery, QueryComponent
from .notquery import NotQuery
from indexing import Index, Posting

class AndQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        QueryComponent.__init__(self)
        self.components = components

    def get_postings(self, index : Index) -> list[Posting]:
        # TODO: program the merge for an AndQuery, by gathering the postings of the composed QueryComponents and
		# intersecting the resulting postings.
        a = self.components[0].get_postings(index)
        for i in range(len(self.components)-1):
            b = self.components[i+1].get_postings(index)
            if self.components[i].polarity + self.components[i+1].polarity == 2:
                a = self.__AND(a, b)
            elif self.components[i].polarity + self.components[i+1].polarity == 0:
                a = OrQuery(self.components[i:i+2]).get_postings(index)
                continue
            else:
                a = self.__AND_NOT(a, b, self.components[i].polarity)
        return a
    
    def __AND(self, a, b):
        result = []
        a_ptr = 0
        b_ptr = 0
        while a_ptr < len(a) and b_ptr < len(b):

            if a[a_ptr].doc_id == b[b_ptr].doc_id:
                # I wasn't sure how postings would work so I made a new
                result.append(Posting(a[a_ptr].doc_id))
                a_ptr += 1
                b_ptr += 1
            elif a[a_ptr].doc_id < b[b_ptr].doc_id:
                a_ptr += 1
            else:
                b_ptr += 1
        return result

    def __AND_NOT(self, a, b, a_polarity):
        result = []
        a_ptr = 0
        b_ptr = 0

        # case 1: A AND NOT B
        while a_ptr < len(a) and b_ptr < len(b) and a_polarity:
            if a[a_ptr].doc_id == b[b_ptr].doc_id:
                # I wasn't sure how postings would work so I made a new
                a_ptr += 1
                b_ptr += 1
            elif a[a_ptr].doc_id < b[b_ptr].doc_id:
                result.append(Posting(a[a_ptr].doc_id))
                a_ptr += 1
            else:
                b_ptr += 1
        
        # case 2: NOT A AND B
        while a_ptr < len(a) and b_ptr < len(b):
            if a[a_ptr].doc_id == b[b_ptr].doc_id:
                # I wasn't sure how postings would work so I made a new
                a_ptr += 1
                b_ptr += 1
            elif a[a_ptr].doc_id < b[b_ptr].doc_id:
                a_ptr += 1
            else:
                result.append(Posting(b[b_ptr].doc_id))
                b_ptr += 1

        #Case 3: NOT A AND NOT B is already filtered out

        # add the remainder of the postings from positive query
        while a_ptr < len(a) and a_polarity:
                result.append(Posting(a[a_ptr].doc_id))
                a_ptr += 1
        while b_ptr < len(b) and not a_polarity:
                result.append(Posting(b[b_ptr].doc_id))
                b_ptr += 1
        return result


    def __str__(self):
        return " AND ".join(map(str, self.components))