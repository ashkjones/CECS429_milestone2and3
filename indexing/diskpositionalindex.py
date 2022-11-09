from pathlib import Path
import struct
from typing import Iterable

from indexing.termfreqposting import TermFreqPosting
from .postings import Posting
from .index import Index
import sqlite3

class DiskPositionalIndex(Index):
    """An Index can retrieve postings for a term from a data structure associating terms and the documents
    that contain them."""
    def __init__(self, dir : str):
      self.__db_dir = Path(dir, 'vocabTable.db')
      self.__postings = open(Path(dir, 'postings.bin'), 'rb')
      self.__weights = open(Path(dir, 'docWeights.bin'), 'rb')

    @property
    def weights(self):
        return self.__weights

    
    @property
    def postings_file(self):
        return self.__postings

    @property
    def db_dir(self):
        return self.__db_dir


    def get_p_postings(self, term : str) -> Iterable[Posting]:
        """Retrieves a sequence of Postings of documents that contain the given term."""

        postings = []
        #try:
        connection = sqlite3.connect(self.__db_dir)
        cursor = connection.cursor()
        query = f"""SELECT position FROM term_positions
                    where term = '{term}'"""
        cursor.execute(query) 
        temp = cursor.fetchone()
        if temp is None:
            return list()
        else: 
            bin_pos = temp[0]

        self.__postings.seek(bin_pos) # go to the position

        df = struct.unpack('=i', self.__postings.read(4))[0]
        doc_gap = 0
        for i in range(df):
            doc_id = struct.unpack('=i', self.__postings.read(4))[0] + doc_gap
            w_dt = struct.unpack('=d', self.__postings.read(8))[0]
            tf = struct.unpack('=i', self.__postings.read(4))[0]
            p_td = [0]*tf # save space for the positions
            p_gap = 0
            for j in range(tf):
                p_td[j] = struct.unpack('=i', self.__postings.read(4))[0] + p_gap
                p_gap = p_td[j]
            # add to postings list
            postings.append(Posting(doc_id, p_td))
            

        return postings


    def get_np_postings(self, term : str) -> Iterable[Posting]: 
        """Retrieves a sequence of Postings of documents that contain the given term without position."""
        postings = []
        connection = sqlite3.connect(self.__db_dir)
        cursor = connection.cursor()
        query = f"""SELECT position FROM term_positions
                    where term = '{term}'"""
        cursor.execute(query) 
        temp = cursor.fetchone() # this is a band aid 
        if temp is None:
            return list()
        else: 
            bin_pos = temp[0]
        self.__postings.seek(bin_pos) # go to the position

        df = struct.unpack('=i', self.__postings.read(4))[0]
        doc_gap = 0
        for i in range(df):
            doc_id = struct.unpack('=i', self.__postings.read(4))[0] + doc_gap
            # if doc_id >= 36788:
            #     j = 5
            w_dt = struct.unpack('=d', self.__postings.read(8))[0]
            tf = struct.unpack('=i', self.__postings.read(4))[0]

            # we will just read bytes to progress the pointer
            skip = tf * 4
            self.__postings.read(skip)

            # we will be using the special TermFrePosting object
            # to make the work ahead easier. Inherits from Posting so
            # older code will still work
            postings.append(TermFreqPosting(doc_id, tf, w_dt))
            doc_gap = doc_id

        return postings


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