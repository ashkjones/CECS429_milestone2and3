from .querycomponent import QueryComponent
from indexing import Index, Posting

class OrQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        QueryComponent.__init__(self)
        self.components = components

    def get_postings(self, index : Index) -> list[Posting]:
        # TODO: program the merge for an OrQuery, by gathering the postings of the composed QueryComponents and
		# merging the resulting postings.
        a = self.components[0].get_postings(index)
        for i in range(len(self.components)-1):
            b = self.components[i+1].get_postings(index)
            a_ptr = 0
            b_ptr = 0
            result = []
            while a_ptr < len(a) and b_ptr < len(b):
                if a[a_ptr].doc_id == b[b_ptr].doc_id:
                    result.append(Posting(a[a_ptr].doc_id)) 
                    a_ptr += 1
                    b_ptr += 1
                elif a[a_ptr].doc_id < b[b_ptr].doc_id:
                    result.append(Posting(a[a_ptr].doc_id))
                    a_ptr += 1
                else:
                    result.append(Posting(b[b_ptr].doc_id))
                    b_ptr += 1
            # end of one list reached, append the rest of the other list
            while a_ptr < len(a):
                result.append(Posting(a[a_ptr].doc_id))
                a_ptr += 1
            while b_ptr < len(b):
                result.append(Posting(b[b_ptr].doc_id))
                b_ptr += 1
                
            a = result
        return a


    def __str__(self):
        return "(" + " OR ".join(map(str, self.components)) + ")"