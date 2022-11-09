import heapq
import struct
from io import FileIO
from typing import IO
from documents.directorycorpus import DirectoryCorpus
from indexing import Index, TermFreqPosting, DiskPositionalIndex
from numpy import log
from text import TokenProcessor, NoTokenProcessor

class RankedQueryParser():
   
    tokenizer : TokenProcessor = NoTokenProcessor()


    def parse_query(self, query : str, index : DiskPositionalIndex, d : DirectoryCorpus,
        weights: IO, k : int = 10):

        tokens = query.split(' ')
        terms = flatten(list(map(self.tokenizer.process_token, tokens)))

        # accumulator
        A = {}

        # count how many
        for t in terms:
            postings = index.get_np_postings(t)
            df = len(postings)

            # if df is 0, we can continue
            if df == 0:
                continue
            w_qt = log(1 + (len(d)/df))

            for post in postings:
                # it will because np_postings but just incase, we will check
                if isinstance(post, TermFreqPosting):
                    w_dt = post.w_dt
                    if post.doc_id in A:
                        A[post.doc_id] += w_dt*w_qt
                    else:
                        A[post.doc_id] = (w_dt*w_qt)
                else: 
                    raise Exception("Not a TermFreqPost in ranking")
        

        # look at me using a heap as per the instructions

        heap = []
        for doc in A:
            doc_weight = get_weights(doc, weights)
            heapq.heappush(heap, (doc, A[doc]/doc_weight))

        return heapq.nlargest(k, heap, key=value)

def value(pair):
    return pair[1]

def flatten(l):
    return [item for sublist in l for item in sublist]

def get_weights(doc_id : int, weights : IO) -> float: 
   offset = doc_id*8
   weights.seek(offset)
   return struct.unpack("=d", weights.read(8))[0]




        
    




         

      

      





   
