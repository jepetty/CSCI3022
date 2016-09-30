# Jessica Petty
# CSCI 3022
# September 29, 2016
# Assignment 2

from math import log, exp
from collections import defaultdict, Counter
from zipfile import ZipFile
from random import uniform
import re

kNEG_INF = -1e6

kSTART = "<s>"
kEND = "</s>"

kWORDS = re.compile("[a-z]{1,}")
kREP = set(["Bush", "GWBush", "Eisenhower", "Ford", "Nixon", "Reagan"])
kDEM = set(["Carter", "Clinton", "Truman", "Johnson", "Kennedy"])

class OutOfVocab(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)

def sentences_from_zipfile(zip_file, filter_presidents):
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

            if pres in filter_presidents:
                for jj in z.read(ii).decode(errors='replace').split("\n")[3:]:
                    yield jj.lower()

def tokenize(sentence):
    """
    Given a sentence, return a list of all the words in the sentence.
    """
    
    return kWORDS.findall(sentence.lower())

def bigrams(sentence):
    """
    Given a sentence, generate all bigrams in the sentence.
    """
    
    for ii, ww in enumerate(sentence[:-1]):
        yield ww, sentence[ii + 1]




class BigramLanguageModel:

    def __init__(self):
        self._vocab = set([kSTART, kEND])
        self._bigrams = {}
        self._word_count = 2
        self._counted = {}
        self._obama_bigram = []
        self._vocab_final = False

    def train_seen(self, word):
        """
        Tells the language model that a word has been seen.  This
        will be used to build the final vocabulary.
        """
        assert not self._vocab_final, \
            "Trying to add new words to finalized vocab"

        # add new words, keep track of count for words and total unique words
        if word not in self._vocab:
            self._vocab.add(word)
            self._counted[word] = 1
            self._word_count = self._word_count + 1
        else:
            self._counted[word] = self._counted[word] + 1


    def generate(self, context):
        """
        Given the previous word of a context, generate a next word from its
        conditional language model probability.  
        """

        probs = {}
        total_prob = 0
        for word in self._bigrams[context]:
            # calculate the probability of a word given a context
            probs[word] = exp(self.laplace(context,word))
            # keep track of the total probability
            total_prob = total_prob + probs[word]
        # generate a uniform variable to perform simulation
        u = uniform(0, total_prob)
        prob = 0
        # picture this like a timeline -> keep moving up the timeline to a new
        # word until our uniform variable is in a section owned by a word
        for word in probs:
            prob = prob + probs[word]
            if u < prob:
                return word

        # case for when there is no predefined words following this context
        return_word = ""
        max_value = -1
        for word in self._counted:
            if self._counted[word] > max_value:
                # we'll just return the word seen the most often (many ways to do this)
                return_word = word
                max_value = self._counted[word]
        return return_word

            
    def sample(self, sample_size):
        """
        Generate an English-like string from a language model of a specified
        length (plus start and end tags).
        """

        yield kSTART
        next = kSTART
        for ii in range(sample_size):
            next = self.generate(next)
            if next == kEND:
                break
            else:
                yield next
        yield kEND
            
    def finalize(self):
        """
        Fixes the vocabulary as static, prevents keeping additional vocab from
        being added
        """
        
        self._vocab_final = True

    def tokenize_and_censor(self, sentence):
        """
        Given a sentence, yields a sentence suitable for training or testing.
        Prefix the sentence with <s>, generate the words in the
        sentence, and end the sentence with </s>.
        """
        
        yield kSTART
        for ii in tokenize(sentence):
            if ii not in self._vocab:
                raise OutOfVocab(ii)
            yield ii
        yield kEND

    def vocab(self):
        """
        Returns the language model's vocabulary
        """

        assert self._vocab_final, "Vocab not finalized"
        return list(sorted(self._vocab))
        
    def laplace(self, context, word):
        """
        Return the log probability (base e) of a word given its context
        """

        assert context in self._vocab, "%s not in vocab" % context
        assert word in self._vocab, "%s not in vocab" % word

        val = 0.0
        total_count = 0
        for con_word in self._bigrams[context]:
            # find the total number of words associated with a context
            total_count = total_count + self._bigrams[context][con_word]
        # if the word is known, get it's count, otherwise set to 0
        if word in self._bigrams[context]:
            word_count = self._bigrams[context][word]
        else:
            word_count = 0
            # we've never seen this bigram -> track that Obama was the first to use it
            self._obama_bigram.append([context, word])
        # val is defined by the laplace smoothing equation
        val = (word_count + 1)/(total_count + self._word_count)
        return log(val)

    def add_train(self, sentence):
        """
        Add the counts associated with a sentence.
        """

        # make a count of all (context, word)
        for context, word in bigrams(list(self.tokenize_and_censor(sentence))):
            assert word in self._vocab, "%s not in vocab" % word
            assert context in self._vocab, "%s not in vocab" % context
            if context in self._bigrams:
                if word in self._bigrams[context]:
                    # if we've already seen this (context, word) increment it
                    self._bigrams[context][word] = self._bigrams[context][word] + 1
                else:
                    # if we've never seen this word with this context, add it
                    self._bigrams[context][word] = 1
            else:
                # if we've never seen this countext, create it
                self._bigrams[context] = {word: 1}

    def log_likelihood(self, sentence):
        """
        Compute the log likelihood of a sentence, divided by the number of
        tokens in the sentence.
        """

        sent = self.tokenize_and_censor(sentence)
        prob = 0
        first = True
        total = 0
        for word in sent:
            total = total + 1
            # we need to check if it's the first word to do nothing
            if first:
                first = False
            # otherwise add this word's probability to the total probability
            else:
                prob = prob + self.laplace(prev_word, word)
            prev_word = word
        return prob/total


if __name__ == "__main__":
    dem_lm = BigramLanguageModel()
    rep_lm = BigramLanguageModel()

    for target, pres, name in [(dem_lm, kDEM, "D"), (rep_lm, kREP, "R")]:
        for sent in sentences_from_zipfile("../data/state_union.zip", pres):
            for ww in tokenize(sent):
                target.train_seen(ww)
                
        print("Done looking at %s words, finalizing vocabulary" % name)
        target.finalize()
        
        for sent in sentences_from_zipfile("../data/state_union.zip", pres):
            target.add_train(sent)
    
        print("Trained language model for %s" % name)

    with open("../data/2016-obama.txt", encoding='utf8') as infile:
        print("REP\t\tDEM\t\tSentence\n" + "=" * 80)
        for ii in infile:
            if len(ii) < 15: # Ignore short sentences
                continue
            try:
                dem_score = dem_lm.log_likelihood(ii)
                rep_score = rep_lm.log_likelihood(ii)

                print("%f\t%f\t%s" % (dem_score, rep_score, ii.strip()))
            except OutOfVocab:
                None

            
            
