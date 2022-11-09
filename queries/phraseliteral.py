from indexing.postings import Posting
from text import TokenProcessor, NoTokenProcessor, BasicTokenProcessor, StemmingTokenProcessor
from .querycomponent import QueryComponent

class PhraseLiteral(QueryComponent):
    """
    Represents a phrase literal consisting of one or more terms that must occur in sequence.
    """

    tokenizer : TokenProcessor = NoTokenProcessor()

    def __init__(self, terms : list[str]):
        QueryComponent.__init__(self)
        self.terms = [s for s in terms]


    def get_postings(self, index) -> list[Posting]:
        # check if this is a valid PhraseLiteral
        if len(self.terms) == 0:
            return []

        # offset keeps count of space between term positions
        offset = 0

        a = index.get_p_postings(PhraseLiteral.tokenizer.process_token(self.terms[0])[-1]) 

        for i in range(len(self.terms)-1):
            b = index.get_p_postings(PhraseLiteral.tokenizer.process_token(self.terms[i+1])[-1]) 
            a_ptr = 0
            b_ptr = 0
            offset += 1
            result = []
            # preform the merge of posting lists
            while a_ptr < len(a) and b_ptr < len(b):
                if a[a_ptr].doc_id == b[b_ptr].doc_id:
                    
                    # loop through the positions
                    pos = []
                    x = a[a_ptr].positions
                    y = b[b_ptr].positions
                    x_ptr = 0
                    y_ptr = 0
                    while x_ptr < len(x) and y_ptr < len(y):
                        if x[x_ptr] + offset == y[y_ptr]:
                            pos.append(x[x_ptr])
                            x_ptr += 1
                            y_ptr += 1
                        elif x[x_ptr] < y[y_ptr]:
                            x_ptr += 1
                        else:
                            y_ptr += 1
                    if len(pos) > 0:
                        result.append(Posting(a[a_ptr].doc_id, pos))
                    a_ptr += 1
                    b_ptr += 1
                # increment the pointer at the smaller doc_id
                elif a[a_ptr].doc_id < b[b_ptr].doc_id:
                    a_ptr += 1
                else:
                    b_ptr += 1
            a = result
        return a

    def __str__(self) -> str:
        return '"' + " ".join(self.terms) + '"'