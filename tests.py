import re
from indexing import Index, Posting
from porter2stemmer import Porter2Stemmer

stemmer = Porter2Stemmer()
term = "the".split('-')
print(term[0])
print(stemmer.stem(term[0]))