from documents.directorycorpus import DirectoryCorpus
from indexing.index import Index
from queries import SpecialQuery, BooleanQueryParser, TokenController
from text import (BasicTokenProcessor, StemmingTokenProcessor, TokenProcessor,
    NoTokenProcessor, BackStemTokenProcessor, TokenStream, EnglishTokenStream)

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
        d, index = SpecialQuery.new_index(command[1])
    elif command[0] == "vocab":
        SpecialQuery.vocabulary(index)
    else:
        print("Unrecognized command\n")
    # so I guess python isn't Java and needs this line
    return d, index


"""runs all the stuff"""
if __name__ == "__main__":
    # User can change token process at runtime only at beginning
    tokenizer : TokenProcessor = None
    print("Select Token Processor to use: \n 1) None \n 2) Basic \n 3) Stemming \n 4) Other Stemming\n")
    while(True):
        selection = input("Enter selection number: ")
        if selection == "1":
            tokenizer = NoTokenProcessor()
        elif selection == "2":
            tokenizer = BasicTokenProcessor()
        elif selection == "3":
            tokenizer = StemmingTokenProcessor()
        elif selection == "4":
            tokenizer = BackStemTokenProcessor()
        else:
            print("No such option exists\n")
            continue
        TokenController(tokenizer)
        break

    path = input("\nEnter path of corpus directory: ")
    # easy copy and paste
    # /Users/ashleyjones/Documents/CSULB/2022Fall/CECS429/SearchFoundations_Python/MobyDick10Chapters
    # /Users/ashleyjones/Documents/CSULB/2022Fall/CECS429/SearchFoundations_Python/all-nps-sites-extracted

    d, index = SpecialQuery.new_index(path)


    while True: 
        parser = BooleanQueryParser()
        query = input("\nEnter query: ")

        if query[0] == ":": 
            command : list[str] = query[1:].split(' ')
            d, index = execute_special(command, d, index)   
        else:
            postings = parser.parse_query(query).get_postings(index)
            for p in postings:
                print(f"ID {p.doc_id} | Title \"{d.get_document(p.doc_id).title}\" | File: {d.get_document(p.doc_id).name}")
            print(f"Number of Documents: {len(postings)}\n")

            while len(postings) > 0:
                view = input(f"\nView Document (y/n)? " )
                if view[0].lower() == 'y':
                    id = int(input("Enter Document ID: "))
                    stream : TokenStream = EnglishTokenStream(d.get_document(id).get_content())
                    for s in stream:
                        print(s, end= ' ')
                else:
                    break
            

            
