import heapdict
import re

_quote_re = re.compile(r"[\"\']")
string = "1089\'wide"
string = re.sub(_quote_re, "", string)
print(string)