import math
from textblob import TextBlob

"""
TF-IDF Algorithm
Sources:
    https://stevenloria.com/tf-idf/
    https://medium.freecodecamp.org/how-to-process-textual-data-using-tf-idf-in-python-cd2bbc0a94a3
"""


# Computes the 'term frequency' of a word
#   => number of times a word appears in a document blob, divided by the number total of words in the blob.
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)


# Returns the number of documents containing the word 'word'
def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)


# Computes the 'inverse document frequency'
#   => measures how common 'word' is among all documents in 'bloblist'
#   If 'word' is common   => reduces its idf
#   If 'word' is uncommon => raises its idf
def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))


# Computes the 'tf-idf' score
def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


# todo: remove these 3 doc, only for tests purpose
document1 = TextBlob("""Python is a 2000 made-for-TV horror movie directed by Richard
Clabaugh. The film features several cult favorite actors, including William
Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy,
Keith Coogan, Robert Englund (best known for his role as Freddy Krueger in the
A Nightmare on Elm Street series of films), Dana Barron, David Bowe, and Sean
Whalen. The film concerns a genetically engineered snake, a python, that
escapes and unleashes itself on a small town. It includes the classic final
girl scenario evident in films like Friday the 13th. It was filmed in Los Angeles,
 California and Malibu, California. Python was followed by two sequels: Python
 II (2002) and Boa vs. Python (2004), both also made-for-TV films.""")

document2 = TextBlob("""Python, from the Greek word, is a genus of
nonvenomous pythons[2] found in Africa and Asia. Currently, 7 species are
recognised.[2] A member of this genus, P. reticulatus, is among the longest
snakes known.""")

document3 = TextBlob("""The Colt Python is a .357 Magnum caliber revolver formerly
manufactured by Colt's Manufacturing Company of Hartford, Connecticut.
It is sometimes referred to as a "Combat Magnum".[1] It was first introduced
in 1955, the same year as Smith &amp; Wesson's M29 .44 Magnum. The now discontinued
Colt Python targeted the premium revolver market segment. Some firearm
collectors and writers such as Jeff Cooper, Ian V. Hogg, Chuck Hawks, Leroy
Thompson, Renee Smeets and Martin Dougherty have described the Python as the
finest production revolver ever made.""")


# TODO: MOVE TO MAIN
bloblist = [document1, document2, document3]

for i, blob in enumerate(bloblist):

    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    for word, score in sorted_words[:10]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))


