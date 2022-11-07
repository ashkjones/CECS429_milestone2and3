from io import FileIO
import struct
from pathlib import Path
from typing import Iterable
from .positionalinvertedindex import PosInvertedIndex
from .postings import Posting

class DiskIndexWriter:
   """Static class that can write a Positional Inverted Index to a binary file
      in format df_t d tf_td p1 p2 ..."""

   def write_index(index : PosInvertedIndex, dir : str):
      vocab = index.vocabulary()
      path = Path(dir, "postings.bin")
      file = open(path, "wb")
      for term in vocab:
         postings : Iterable[Posting] = index.get_postings(term) # shallow copy
         df = len(postings)
         file.write(struct.pack('>i', df))

         doc_gap = 0

         # loop through the remaining postings
         for post in postings:
            file.write(struct.pack('>i', post.doc_id - doc_gap))
            DiskIndexWriter.__pos_write(post, file)
            doc_gap = post.doc_id


   def __pos_write(post : Posting, file : FileIO):

      positions : list[int] = post.positions # shallow copy
      tf = len(positions)
      file.write(struct.pack('>i', tf))

      pos_gap = 0

      for i in range(1, tf):
         file.write(struct.pack('>i', positions[i] - pos_gap))
         pos_gap = positions[i]


         

         
      

             

