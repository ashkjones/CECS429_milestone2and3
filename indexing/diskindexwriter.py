from io import FileIO
from pathlib import Path
from typing import Iterable
from .positionalinvertedindex import PosInvertedIndex
from .postings import Posting
import struct
import sqlite3


class DiskIndexWriter:
   """Static class that can write a Positional Inverted Index to a binary file
      in format df_t d tf_td p1 p2 ..."""

   def write_index(index : PosInvertedIndex, dir : str):
      vocab = index.vocabulary()
      bin_path = Path(dir, "postings.bin")
      db_path = Path(dir, "search_engine.db")
      file = open(bin_path, "wb")


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
         byte_pos = file.tell()
         cursor.execute(f"""INSERT into term_positions('term', 'position')
                              VALUES
                              ('{term}', {byte_pos})""")

         postings : Iterable[Posting] = index.get_postings(term) # shallow copy
         df = len(postings)
         file.write(struct.pack('>i', df))

         doc_gap = 0

         # loop through the remaining postings
         for post in postings:
            file.write(struct.pack('>i', post.doc_id - doc_gap))
            DiskIndexWriter.__pos_write(post, file)
            doc_gap = post.doc_id

      connection.commit()
      connection.close()
      file.close()

      # except:
      #    print("Writing Index to file failed.")


   def __pos_write(post : Posting, file : FileIO):

      positions : list[int] = post.positions # shallow copy
      tf = len(positions)
      file.write(struct.pack('>i', tf))

      pos_gap = 0

      for i in range(0, tf):
         file.write(struct.pack('>i', positions[i] - pos_gap))
         pos_gap = positions[i]


         

         
      

             

