import heapq
from io import FileIO
from helperfunction.mathfunctions import get_weights
from indexing import Index, TermFreqPosting, DiskPositionalIndex
from numpy import log
from text import TokenProcessor, NoTokenProcessor

class RankedQueryParser():
   
    _tokenizer : TokenProcessor = NoTokenProcessor()

    
    @property
    def tokenizer():
        return RankedQueryParser._tokenizer

    @tokenizer.setter
    def tokenizer(tokenizer : TokenProcessor):
        RankedQueryParser._tokenizer = tokenizer

    def parse_query(self, query : str, index : DiskPositionalIndex, k : int = 10):

        tokens = query.split(' ')
        terms = flatten(list(map(self._tokenizer.process_token, tokens)))

        # accumulator
        A = {}

        # count how many
        for t in terms:
            postings = index.get_np_postings(t)
            df = len(postings)

            # if df is 0, we can continue
            if df == 0:
                continue
            w_qt = log(1 + (len(tokens)/df))

            for post in postings:
                # it will be but just incase, we will check
                if isinstance(post, TermFreqPosting):
                    w_td = 1 + log(post.tf)
                    if post.doc_id in A:
                        A[post.doc_id] = w_td*w_qt
                    else:
                        A[post.doc_id] = (w_td*w_qt)
                else: 
                    raise Exception("Not a TermFreqPost in ranking")
        

        # look at me using a heap as per the instructions

        heap = []
        for doc in A:
            doc_weight = get_weights(doc, index.weights)
            heapq.heappush(heap, (doc, A[doc]/doc_weight))

        return heapq.nlargest(k, heap, key=value)

def value(pair):
    return pair[1]

def flatten(l):
    return [item for sublist in l for item in sublist]




        
    




         

      

      





   
