import lightrdf
import re

parser = lightrdf.xml.Parser()
word = input()
word = re.sub(r" +", "_", word)
print(word)
with open("ontologie_lab.owl", "rb") as f:
    for triple in parser.parse(f, base_iri=None):
        for t in triple:
            if word in t:
                print(triple)