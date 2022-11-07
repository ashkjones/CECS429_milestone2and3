from pathlib import Path
import struct
from typing import Iterable
from .postings import Posting
from .index import Index
import sqlite3

class DiskPositionalIndex(Index):
    """An Index can retrieve postings for a term from a data structure associating terms and the documents
    that contain them."""
    def __init__(self, dir : str):
      self.__db_dir = Path(dir, 'search_engine.db')
      self.__postings = open(Path(dir, 'postings.bin'), 'rb')

    def get_postings(self, term : str) -> Iterable[Posting]:
        """Retrieves a sequence of Postings of documents that contain the given term."""

        postings = []
        #try:
        connection = sqlite3.connect(self.__db_dir)
        cursor = connection.cursor()
        query = f"""SELECT position FROM term_positions
                    where term = '{term}'"""
        thing = cursor.execute(query) 
        bin_pos = cursor.fetchone()[0] # this is a band aid 

        self.__postings.seek(bin_pos) # go to the position

        df = struct.unpack('>i', self.__postings.read(4))[0]
        doc_gap = 0
        for i in range(df):
            doc_id = struct.unpack('>i', self.__postings.read(4))[0] + doc_gap
            tf = struct.unpack('>i', self.__postings.read(4))[0]
            p_td = [0]*tf # save space for the positions
            p_gap = 0
            for j in range(tf):
                p_td[j] = struct.unpack('>i', self.__postings.read(4))[0] + p_gap
                p_gap = p_td[j]
            # add to postings list
            postings.append(Posting(doc_id, p_td))

        return postings
        # except:
        #     print("Could not retrieve postings")
        #     return list()

    def vocabulary(self) -> list[str]:
        """A (sorted) list of all terms in the index vocabulary."""
        try:
            connection = sqlite3.connect(self.__db_dir)
            cursor = connection.cursor()
            cursor.execute("SELECT term FROM term_positions")
            terms = cursor.fetchall()

            connection.close()
            return terms
        except:
            print("Database connection failed")
            return list()