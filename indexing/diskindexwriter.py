from io import FileIO
from math import sqrt
from pathlib import Path
from typing import Iterable

from numpy import log
from .positionalinvertedindex import PosInvertedIndex
from .postings import Posting
import struct
import sqlite3


class DiskIndexWriter:
   """Static class that can write a Positional Inverted Index to a binary file
      in format df_t d tf_td p1 p2 ..."""

   def write_index(index : PosInvertedIndex, dir : str):
      vocab = index.vocabulary()
      new_folder = Path(dir, "index")
      if not new_folder.exists():
         Path.mkdir(new_folder)
      db_path = Path(new_folder, "vocabTable.db")
      post_path = Path(new_folder, "postings.bin")
      post_path.unlink(True)
      post_file = open(post_path, "wb")
      dw_path = Path(new_folder, "docWeights.bin")
      dw_path.unlink(True)
      dw_file = open(dw_path, "wb")

      l_helper = {}


      connection = sqlite3.connect(db_path)
      cursor = connection.cursor()
      print("Connected to Database")
      cursor.execute("DROP TABLE IF EXISTS term_positions")

      table = """ CREATE TABLE term_positions (
               term VARCHAR(255) NOT NULL,
               position INT NOT NULL
               ); """

      cursor.execute(table)
      for term in vocab:

         # Let's record the term byte position to the database
         byte_pos = post_file.tell()
         cursor.execute(f"""INSERT into term_positions('term', 'position')
                              VALUES
                              ('{term}', {byte_pos})""")

         postings : Iterable[Posting] = index.get_p_postings(term) # shallow copy
         df = len(postings)
         post_file.write(struct.pack('=i', df))

         doc_gap = 0

         # loop through the remaining postings
         
         for post in postings:
            post_file.write(struct.pack('=i', post.doc_id - doc_gap))
            w_dt = 1 + log(DiskIndexWriter.__pos_write(post, post_file))
            doc_gap = post.doc_id

            if post.doc_id in l_helper:
               l_helper[post.doc_id] += w_dt*w_dt
            else:
               l_helper[post.doc_id] = w_dt*w_dt
      
      for i in sorted(l_helper.keys()):
         dw_file.write(struct.pack('=d', sqrt(l_helper[i])))

      connection.commit()
      connection.close()
      post_file.close()
      dw_file.close()

      # except:
      #    print("Writing Index to file failed.")


   def __pos_write(post : Posting, file : FileIO):

      positions : list[int] = post.positions # shallow copy
      tf = len(positions)
      file.write(struct.pack('=i', tf))

      pos_gap = 0

      for i in range(0, tf):
         file.write(struct.pack('=i', positions[i] - pos_gap))
         pos_gap = positions[i]

      return tf


         

         
      

             

