from .postings import Posting

class TermFreqPosting(Posting):
   """Special Type of Posting that saves term frequency and no positions"""
   def __init__(self, doc_id, tf, w_dt = 0):
      super().__init__(doc_id)
      self.tf = tf
      self.w_dt = w_dt