from queries.tokencontroller import TokenController
from text import StemmingTokenProcessor
from stats.helperfunctions import *

"""This program builds an index over the .txt and .json files in a provided
    directory. The program also executes user provides queries."""

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

    print('bloop') # very important part of my code
    

def milestone3():
    tokenizer = StemmingTokenProcessor()
    TokenController(tokenizer)
    while(True):
        choice = input(f"1. Build index.\n2. Query Index.\n3. Single-Query statistics. \n4. Multi-query statistics. \n")
        corpus_path = input("Enter corpus path: ")
        if choice == '1':
            build_index(corpus_path)
        elif choice == '2':
            query_index(corpus_path)
        elif choice == '3':
            run_single(corpus_path)
        elif choice == '4':
            multi_stats(corpus_path)
        else:
            print("Selection not recognized. Exiting...")
            exit()

    # /Users/ashleyjones/Documents/milestoneexample/cranfield
    # /Users/ashleyjones/Documents/milestoneexample/relevance_parks
            
if __name__ == "__main__":
    milestone3()

