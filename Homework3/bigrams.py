# Jessica Petty
# CSCI 3022
# Homework 3
# October 13, 2016
import re
import operator
from collections import Counter
from zipfile import ZipFile

from numpy import array
from scipy import zeros
from scipy.stats import chisquare
from scipy.stats.distributions import chi2

kWORDS = re.compile("[a-z]{1,}")
kSTOPWORDS = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'yo',
                  'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his',
                  'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
                  'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
                  'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
                  'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
                  'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
                  'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
                  'with', 'about', 'against', 'between', 'into', 'through', 'during',
                  'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in',
                  'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
                  'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
                  'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
                  'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
                  's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 've', 'm'])

def bigrams(sentence):
    """
    Given a sentence, generate all bigrams in the sentence.
    """
    
    for ii, ww in enumerate(sentence[:-1]):
        yield ww, sentence[ii + 1]

def tokenize(sentence):
    """
    Given a sentence, return a list of all the words in the sentence.
    """
    
    return kWORDS.findall(sentence.lower())

def sentences_from_zipfile(zip_file):
    """
    Given a zip file, yield an iterator over the lines in each file in the
    zip file.
    """
    with ZipFile(zip_file) as z:
        for ii in z.namelist():
            try:
                pres = ii.replace(".txt", "").replace("state_union/", "").split("-")[1]
            except IndexError:
                continue

            for jj in z.read(ii).decode(errors='replace').split("\n")[3:]:
                yield jj.lower()

def chisquare_pvalue(obs, ex):
    """
    Given a 2x2 contingency table both observed and expected, returns the
    corresponding chisquared p-value.

    @param obs An array (list of lists or numpy array) of observed values
    @param obs An array (list of lists or numpy array) of expected values
    """

    _sum = 0
    for i in range(0,2):
        for j in range(0,2):
            _sum = _sum + (obs[i][j] - ex[i][j])**2/ex[i][j]
    chi = 1 - chi2.cdf(_sum,1)
    return chi

class BigramFinder:
    """
    Finds bigrams in a stream of text.
    """

    def __init__(self, min_unigram = 10, max_unigram = 150, min_ngram = 5,
                 exclude=[]):
        """
        Instantiates the class.

        @param min_ngram Ignore bigrams that appear fewer than this many times 

        @param max_unigram Ignore words that appear more than this many times

        @param min_unigram Ignore words that appear fewer than this many times

        @param exclude Don't add words from this set to bigrams
    
        """
        self._exclude = set(exclude)

        self._max_unigram = max_unigram
        self._min_unigram = min_unigram
        self._min_ngram = min_ngram

        self._vocab = None
        self._bigram_reverse = {}

        # You may want to add additional data structures here.

        self._unigram = Counter()
        self._bigram_count = Counter()
        self._bigram_left = Counter()
        self._bigram_right = Counter()

    def observed_and_expected(self, bigram):
        """
        Compute the observed and expected counts for a bigram

        @bigram A tuple containing the words to score
        """
        #***** total bigram count correct, obs1, obs3 *******

        ll, rr = bigram
        total_bigram_count = sum(self._bigram_count.values())

        obs1 = self._bigram_reverse[rr][ll]
        obs2 = self._bigram_right[rr] - self._bigram_reverse[rr][ll]
        obs3 = self._bigram_left[ll] - self._bigram_reverse[rr][ll]
        obs4 = total_bigram_count - obs1 - obs3 - obs2
        obs = array([[obs1, obs2], [obs3, obs4]])


        ex1 = (self._bigram_left[ll]*self._bigram_right[rr])/total_bigram_count
        ex2 = ((total_bigram_count - self._bigram_left[ll])*self._bigram_right[rr])/total_bigram_count
        ex3 = (self._bigram_left[ll]*(total_bigram_count - self._bigram_right[rr]))/total_bigram_count
        ex4 = ((total_bigram_count - self._bigram_left[ll])*(total_bigram_count - self._bigram_right[rr]))/total_bigram_count
        ex = array([[ex1, ex2], [ex3, ex4]])

        return obs, ex
        
    def score(self, bigram):
        """
        Compute the chi-square probability of a bigram being dependent.
        If either word of a bigram is in the "exclude" list, return 1.0.

        @bigram A tuple containing the words to score
        """

        # you shouldn't need to edit this function
        if any(x in self._exclude for x in bigram):
            return 1.0

        obs, ex = self.observed_and_expected(bigram)
                
        return chisquare_pvalue(obs, ex)

    def vocab_scan(self, sentence):
        """
        Given a sentence, scan all of its words and add up their counts.
        This will be used to finalize the vocabulary later.
        """

        # Don't modify this function.        
        for ii in sentence:
            self._unigram[ii] += 1

    def vocab(self):
        """
        Return the finder's vocab
        """

        # Don't modify this function.        
        return self._vocab

    def finalize(self):
        """
        Creates the vocabulary of for later processing.  Filters low frequency
        and high frequency words.
        """

        # Don't modify this function.
        self._vocab = set(x for x in self._unigram if self._unigram
                          if self._unigram[x] >= self._min_unigram and
                          self._unigram[x] <= self._max_unigram and
                          x not in self._exclude)
    
    def add_sentence(self, sentence):
        """
        Add the counts for a sentence (assumed to be iterable) so that we can
        then score bigrams.
        """
        assert self._vocab is not None, "Adding counts before finalizing vocabulary"
        
        for ll, rr in bigrams(sentence):
            self._bigram_count[(ll,rr)] += 1
            self._bigram_left[ll] += 1
            self._bigram_right[rr] += 1
            if (ll in self._vocab) & (rr in self._vocab):
                assert ll in self._vocab, "%s not in vocab" % ll
                assert rr in self._vocab, "%s not in vocab" % rr
                if rr in self._bigram_reverse:
                    if ll in self._bigram_reverse[rr]:
                        self._bigram_reverse[rr][ll] = self._bigram_reverse[rr][ll] + 1
                    else:
                        self._bigram_reverse[rr][ll] = 1
                else:
                    self._bigram_reverse[rr] = {ll:1}

    def valid_bigrams(self):
        """
        Return an iterator over the bigrams that have been seen enough to get a
        score.
        """
        valid_grams = []
        for rr in self._bigram_reverse:
            for ll in self._bigram_reverse[rr]:
                if self._bigram_reverse[rr][ll] >= self._min_ngram:
                    valid_grams.append((ll,rr))
        return valid_grams
        
    def sorted_bigrams(self):
        """
        Return n-grams sorted by the probability of being an n-gram.  Should
        yield a tuple of words in bigram and the p-value of the bigram.
        """
        
        # You should not need to modify this function
        
        d = {}
        for ngram in self.valid_bigrams():
            d[ngram] = self.score(ngram)

        for ngram, score in sorted(d.items(), key=operator.itemgetter(1), reverse=True):
            yield ngram, score

if __name__ == "__main__":
    bf = BigramFinder(exclude=kSTOPWORDS)
    
    for sent in sentences_from_zipfile("../data/state_union.zip"):
        bf.vocab_scan(tokenize(sent))

    bf.finalize()
    
    for sent in sentences_from_zipfile("../data/state_union.zip"):
        bf.add_sentence(tokenize(sent))
                
    for ngram, score in list(bf.sorted_bigrams())[:100]:
        print("%f\t%s\t%s\t" % (score, ngram[0], ngram[1]))
