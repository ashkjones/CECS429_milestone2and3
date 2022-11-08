from .postings import Posting

class TermFreqPosting(Posting):
   """Special Type of Posting that saves term frequency and no positions"""
   def __init__(self, doc_id, tf):
      super().__init__(doc_id)
      self.tf = tf