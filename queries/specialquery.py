from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, PosInvertedIndex
from text import TokenProcessor, EnglishTokenStream, TokenStream
from time import time
from text.notokenprocessor import NoTokenProcessor


"""Handles special queries"""
class SpecialQuery:

    # the singleton class TokenController will set this 
    _tokenizer : TokenProcessor = NoTokenProcessor()
    index : Index = None

    @property
    def tokenizer():
        return SpecialQuery._tokenizer

    @tokenizer.setter
    def tokenizer(tokenizer : TokenProcessor):
        SpecialQuery._tokenizer = tokenizer


    '''Returns the stemmed token if there is a tokenizer set'''
    @staticmethod
    def stem(token : str) -> str:
        return SpecialQuery.tokenizer.process_token(token)


    '''Indexes a new corpus at a given path'''
    @staticmethod
    def new_index(directory : str) -> tuple[DirectoryCorpus, Index]:
        corpus_path = Path(directory)
        start = time()
        d = DirectoryCorpus.load_text_directory(corpus_path)
        # Build the index over this directory.
        print(f'Found {len(d)} Documents.')
        print(" Indexing...")
        
        index = SpecialQuery._index_corpus(d)
        print(f"\nIndexing Complete. Time elapsed: {time()-start:.2f}s")
        return d, index

    @staticmethod
    def _index_corpus(corpus : DocumentCorpus) -> Index:  
        index : Index = PosInvertedIndex()
        for d in corpus:
            stream : TokenStream = EnglishTokenStream(d.get_content())
            pos : int = 0
            for s in stream:
                terms : list[str] = SpecialQuery.tokenizer.process_token(s)
                # skip over empty strings
                if not bool(terms[0]):
                    continue
                # the token processor might return several terms
                for t in terms:
                    index.add_term(t, d.id, pos)
                pos += 1

        return index

    '''Prints first 1000 terms and number of terms in index'''
    @staticmethod
    def vocabulary(index : Index):
        vocab = index.vocabulary()
        print("First 1000 terms in index:")
        if len(vocab) < 1000:
            show = len(vocab)
        else:
            show = 1000
        for i in range(show):
            print(vocab[i])
        print(f"\nTotal number of terms: {len(vocab)}")

    '''Exits program'''
    @staticmethod
    def exit_program():
        print("Exiting program...")
        quit()


