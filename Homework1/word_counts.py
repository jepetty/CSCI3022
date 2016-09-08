# Jessica Petty
# CSCI 3022
# Homework 1
# September 8, 2016

from collections import Counter
from zipfile import ZipFile
import re

kWORDS = re.compile("[a-z]{4,}")

def text_from_zipfile(zip_file):
    """
    Given a zip file, yield an iterator over the text in each file in the
    zip file.
    """
    with ZipFile(zip_file,'r') as myzip:
        files = myzip.namelist()
        for curr_file in files:
            if "README" not in curr_file:
                with myzip.open(curr_file) as speech:
                    yield speech.read().decode("utf-8","ignore")

def words(text):
    """
    Return all words in a string, where a word is four or more contiguous
    characters in the range a-z or A-Z.  The resulting words should be
    lower case.
    """
    return re.findall(kWORDS,text.lower())

def accumulate_counts(words, total=Counter()):
    """
    Take an iterator over words, add the sum to the total, and return the
    total.

    @words An iterable object that contains the words in a document
    @total The total counter we should add the counts to
    """
    assert isinstance(total, Counter)
    for word in words:
        total[word] += 1
    return total

if __name__ == "__main__":
    # You should not need to modify this part of the code
    total = Counter()
    for tt in text_from_zipfile("../data/state_union.zip"):
        total = accumulate_counts(words(tt), total)

    for ii, cc in total.most_common(100):
        print("%s\t%i" % (ii, cc))

