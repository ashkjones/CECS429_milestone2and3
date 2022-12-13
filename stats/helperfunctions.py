from pathlib import Path
import time
from typing import TextIO

from matplotlib import pyplot as plt
from documents.directorycorpus import DirectoryCorpus
from indexing import Index, DiskPositionalIndex
from queries import BooleanQueryParser, RankedQueryParser, SpecialQuery
from stats.ranking import Ranking
from text import englishtokenstream, TokenStream


th = 0.9

def execute_special(command : list[str], d : DirectoryCorpus, index : Index): 
    """Handles the special queries"""
    
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


def boolean_retrieval(d : DirectoryCorpus, index : Index):
    """Handles boolean queries"""
    while True: 
        parser = BooleanQueryParser()
        query = input("\nEnter query: ")

        if query[0] == ":": 
            command : list[str] = query[1:].split(' ')
            execute_special(command, d, index)   
        else:
            postings = parser.parse_query(query).get_postings(index)
            for p in postings:
                print(f"ID {p.doc_id} | \"{d.get_document(p.doc_id).title}\" | {d.get_document(p.doc_id).name}")
            print(f"Number of Documents: {len(postings)}\n")
            view_doc(postings, d)


def view_doc(scored : any, d : DirectoryCorpus):
    """Prompts users and shows documents using doc_id"""

    while len(scored) > 0:
        view = input(f"\nView Document (y/n)? " )
        if view[0].lower() == 'y':
            id = int(input("Enter Document ID: "))
            stream : TokenStream = englishtokenstream(d.get_document(id).get_content())
            for s in stream:
                print(s, end= ' ')
        else:
            break


def ranked_retrieval(d : DirectoryCorpus, index : Index): 
    """Handles ranked retrieval queries"""
    k = 10
    parser = RankedQueryParser()
    choice = input("Mode:\n1. Default\n2. Vocab Elimination\n") 
    if choice == "1":
        threshold = 0
    elif choice == "2":
        threshold = th
    else: 
        print("Selection not recognized...")
        return
    while True:

        query = input("\nEnter query: ")

        # change this line if not DPI but we need weights as IO
        weights = index.weights

        if query[0] == ":": 
            command : list[str] = query[1:].split(' ')
            execute_special(command, d, index)  
            if command[0] == 'index':
                query_index() 
        else:
            top_docs = parser.parse_query(query, index, d, weights, k, threshold)
            for i in range(len(top_docs)):
                doc = top_docs[i]
                print(f"{i+1}. ID {doc[0]} | \"{d.get_document(doc[0]).title}\" | {d.get_document(doc[0]).name} | Score: {doc[1]:.4f}")
            view_doc(top_docs, d)


def build_index(corpus_path : str):
    """Builds new index"""
    SpecialQuery.new_index(corpus_path)



def query_index(corpus_path : str):
    """Handles query index selection"""

    d : DirectoryCorpus = DirectoryCorpus.load_text_directory(corpus_path, 1)
    print("num documents =", len(d))
    path = Path(corpus_path, "index")
    index = DiskPositionalIndex(path)

    choice = (input(f"\n1. Boolean retrieval.\n2. Ranked retrieval.\n"))
    if choice == '1':
        boolean_retrieval(d, index)
    elif choice == '2':
        ranked_retrieval(d, index)
    else:
        print("Selection not recognized. Exiting...")
        exit()

def multi_stats(corpus_path):
    """Calculates search engine statistics over multiple queries in text file"""

    choice = (input(f"\n1. Normal \n2. Vocab Elimination \n"))
    if choice == '1':
        map, mrt, tp = run_queries(corpus_path)
        print(f"\nMAP = {map}\nMRT = {mrt}\nthroughput = {tp}")
    elif choice == '2':
        map, mrt, tp = run_queries(corpus_path, Ranking.VOCAB_ELIM)
        print(f"\nMAP = {map}\nMRT = {mrt}\nthroughput = {tp}")
    else:
        print("Selection not recognized. Exiting...")
        exit()


def run_queries(path : str, flag = Ranking.DEFAULT):
    k = 50
    if flag == Ranking.VOCAB_ELIM:
        threshold = th
    else:
        threshold = 0
    d : DirectoryCorpus = DirectoryCorpus.load_text_directory(path, 1)
    index_path = Path(path, "index")
    index = DiskPositionalIndex(index_path)

    # copy the queries into a list
    query_path = Path(path, "relevance/queries")
    q_file = open(query_path, "r")
    queries = q_file.readlines()
    q_file.close()    
    
    # get the relevant docs for each query
    rel_path = Path(path, "relevance/qrel")
    rel_file = open(rel_path, "r")
    relevant = iter(rel_file.readlines())   # iterator so we can use yield
    rel_file.close()  

    elapsed = 0
    sum = 0

    # yes, there is redundant code. However, checking the flag in side the loop is slower
    parser = RankedQueryParser()
    for q in queries:
        # we will only add time the query is running,
        start = time.time()
        top_docs = parser.parse_query(q, index, d, index.weights, k, threshold)
        elapsed += time.time() - start
        # i probably want to make d a global so I don't need to keep passing it
        sum += avg_precision(d, top_docs, set(next(relevant).split()))
    return sum/len(queries), elapsed/len(queries), len(queries)/elapsed


def avg_precision(d : DirectoryCorpus, documents, rel_set):
    """"Calculates the average precision for query results"""
    rel_results = 0
    sum = 0
    for i in range(len(documents)):
        name = d.get_document(documents[i][0]).name

        # remove leading 0 and extension
        for j in range(len(name)):
            if name[j] != "0":
                name = name[j:-1]
                break
        for j in range(len(name)-1, -1, -1):
            if name[j] == ".":
                name = name[0:j]
                break
        if name in rel_set:
            rel_results += 1
            sum += rel_results/(i+1)
    else:
        return sum/len(rel_set)


def run_single(path):
    """Finds Statistics for Single Query"""
    threshold = th
    k = 50
    # change this line if not DPI but we need weights so...
    d : DirectoryCorpus = DirectoryCorpus.load_text_directory(path, 1)
    index = DiskPositionalIndex(Path(path, "index"))
    weights = index.weights 

    choice = input("1. Manual Entry\n2. First Query\n")

    if choice == "1":
        query = input("Enter query: ")
        relevant = set(input("Enter relevant docs: ").split())
    elif choice == "2":
        # copy the query
        q_file = open(Path(path, "relevance/queries"), "r")
        query = q_file.readline()
        q_file.close() 

        # get the relevant docs for each query
        rel_file = open(Path(path, "relevance/qrel"), "r")
        relevant = set(rel_file.readline().split())
        rel_file.close() 
    else:
        print("Selection not recognized. Exiting...")
        return 

    parser = RankedQueryParser()
    top_docs = parser.parse_query(query, index, d, weights, k)
    file = open("query_results.txt", "w")
    file.write("Default Results")
    print("Default Results")
    precision_recall(d, top_docs, relevant, Ranking.DEFAULT, file)
    mrt_calc(query, index, d, weights, k, parser, file)

    top_docs = parser.parse_query(query, index, d, weights, k, threshold)
    file.write("Vocab Elimination Results")
    print("Vocab Elimination Results")
    precision_recall(d, top_docs, relevant, Ranking.VOCAB_ELIM, file)
    mrt_calc(query, index, d, weights, k, parser, file)

    file.close()

    precision_recall
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title(f"Precision-Recall for query \"{query}\"")
    plt.legend()
    plt.savefig('precision_recall.png')
    plt.show()


def precision_recall(d : DirectoryCorpus, documents : list, rel_set : set, flag, file : TextIO): 
    """Creates the precision-recall graph, marks which results are relevant, and calculates
        average precisions. Data is saved to files."""
    k_max = len(documents)
    num_rel = len(rel_set)
    rel_results = 0
    sum = 0
    x_d = [0] * (k_max + 1) # extra space for k = 0
    y_d = [0] * (k_max + 1)
    for k in range(1,k_max+1):
        doc = d.get_document(documents[k-1][0])
        name = doc.name
        # remove leading 0 and extension
        for j in range(len(name)):
            if name[j] != "0":
                name = name[j:-1]
                break
        for j in range(len(name)-1, -1, -1):
            if name[j] == ".":
                name = name[0:j]
                break
        if name in rel_set:
            rel_results += 1
            sum += rel_results/(k)
            print(f"\tRelevant: {doc.name} at index {k}")
            file.write(f"\n{k}. RELEVANT | {doc.name} | Score: {documents[k-1][1]:.4f}")
        else:
            file.write(f"\n{k}.          | {doc.name} | Score: {documents[k-1][1]:.4f}")
        x_d[k] = rel_results/num_rel
        y_d[k] = rel_results/(k)

    print(f"Average precision for this query: {sum/num_rel}")
    file.write((f"\nAverage precision for this query: {sum/num_rel}"))

    plt.plot(x_d, y_d, label = f"{flag.name}")


# yes I realize this runs the query 31 times because ran it previously but whatever
def mrt_calc(query : str, index : Index, d : DirectoryCorpus, weights, k : int,
        parser : RankedQueryParser, file : TextIO) -> tuple[float, float]:
    """Calculates the mean response time and throughput by running a given query 30 times."""
    start = time.time()
    n = 30
    for _ in range(n):
        parser.parse_query(query, index, d, weights, k)
    total = time.time() - start

    mean_response = total/n
    throughput = 1/mean_response
    print(f"Mean response time: {mean_response}\nThroughput: {throughput}\n")
    file.write(f"\nMean response time: {mean_response}\nThroughput: {throughput}\n")

    return mean_response, throughput