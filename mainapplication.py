from pathlib import Path
from typing import Iterable
from documents.directorycorpus import DirectoryCorpus
from indexing import Index, DiskIndexWriter, DiskPositionalIndex, Posting
from queries import SpecialQuery, BooleanQueryParser, TokenController, RankedQueryParser
from text import (StemmingTokenProcessor, TokenProcessor, TokenStream, EnglishTokenStream)

"""This program builds an index over the .txt and .json files in a provided
    directory. The program also executes user provides queries."""

"""Handles the special queries"""
def execute_special(command : list[str], d : DirectoryCorpus, index : Index): 
    length = len(command)
    if length > 2:
        print("Unrecognized command\n")
    if command[0] == "quit":
        SpecialQuery.exit_program()
    elif command[0] == "stem" and length == 2:
        print(SpecialQuery.stem(command[1]))
    elif command[0] == "index" and length == 2:
        SpecialQuery.new_index(command[1])
    elif command[0] == "vocab":
        SpecialQuery.vocabulary(index)
    else:
        print("Unrecognized command\n")
    # so I guess python isn't Java and needs this line


def boolean_retrieval(d : DirectoryCorpus, index : Index):
    while True: 
        parser = BooleanQueryParser()
        query = input("\nEnter query: ")

        if query[0] == ":": 
            command : list[str] = query[1:].split(' ')
            execute_special(command, d, index)   
        else:
            postings = parser.parse_query(query).get_postings(index)
            for p in postings:
                print(f"ID {p.doc_id} | Title \"{d.get_document(p.doc_id).title}\" | File: {d.get_document(p.doc_id).name}")
            print(f"Number of Documents: {len(postings)}\n")
            view_doc(postings, d)


def view_doc(scored : any, d : DirectoryCorpus):
    while len(scored) > 0:
        view = input(f"\nView Document (y/n)? " )
        if view[0].lower() == 'y':
            id = int(input("Enter Document ID: "))
            stream : TokenStream = EnglishTokenStream(d.get_document(id).get_content())
            for s in stream:
                print(s, end= ' ')
        else:
            break


def ranked_retrieval(d : DirectoryCorpus, index : Index): 
    while True:
        parser = RankedQueryParser()
        query = input("\nEnter query: ")

        if query[0] == ":": 
            command : list[str] = query[1:].split(' ')
            execute_special(command, d, index)  
            if command[0] == 'index':
                query_index() 
        else:

            # this needs to be DPI or cannot calculate ranks
            if not isinstance(index, DiskPositionalIndex):
                print("Cannot do ranked retrieval without weights file")
                exit(1)
            top_docs = parser.parse_query(query, index)
            for i in range(len(top_docs)):
                doc = top_docs[i]
                print(f"{i+1}. ID {doc[0]} | Title \"{d.get_document(doc[0]).title}\" | File: {d.get_document(doc[0]).name} | Score: {doc[1]:.4f}")
            view_doc(top_docs, d)



def build_index(corpus_path : str):
    SpecialQuery.new_index(corpus_path)



def query_index(corpus_path : str):
    d : DirectoryCorpus = DirectoryCorpus.load_text_directory(corpus_path)
    path = Path(corpus_path, "index")
    index = DiskPositionalIndex(path)

    choice = (input(f"\n1. Boolean retrieval.\n2. Ranked retrieval.\n"))
    if choice == '1':
        boolean_retrieval(d, index)
    elif choice == '2':
        ranked_retrieval(d, index)
    else:
        print("Selection not recognized. Please try again.")


def milestone2():
    tokenizer = StemmingTokenProcessor()
    TokenController(tokenizer)

    choice = input(f"\n1. Build index.\n2. Query index.\n")

    corpus_path = input("\nEnter corpus path: ")
    if choice == '1':
        build_index(corpus_path)
    elif choice == '2':
        query_index(corpus_path)
    else:
        print("Selection not recognized. Exiting...")
        exit()


    # easy copy and paste
    # /Users/ashleyjones/Documents/CSULB/2022Fall/CECS429/SearchFoundations_Python/MobyDick10Chapters
    # /Users/ashleyjones/Documents/CSULB/2022Fall/CECS429/SearchFoundations_Python/all-nps-sites-extracted

    print('bloop')

            
if __name__ == "__main__":
    milestone2()

