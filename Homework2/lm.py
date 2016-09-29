from math import log, exp
from collections import defaultdict, Counter
from zipfile import ZipFile
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
        # Add your code here!
        # Bigram counts
        self._vocab_final = False

    def train_seen(self, word):
        """
        Tells the language model that a word has been seen.  This
        will be used to build the final vocabulary.
        """
        assert not self._vocab_final, \
            "Trying to add new words to finalized vocab"

        if word not in self._vocab:
            self._vocab.add(word)
            self._word_count = self._word_count + 1


    def generate(self, context):
        """
        Given the previous word of a context, generate a next word from its
        conditional language model probability.  
        """

        # Add your code here.  Make sure to the account for the case
        # of a context you haven't seen before and Don't forget the
        # smoothing "+1" term while sampling.

        # Your code here
        return "the"
            
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

        #the nation
        # Add your code here
        val = 0.0
        total_count = 0
        for con_word in self._bigrams[context]:
            total_count = total_count + self._bigrams[context][con_word]
        if word in self._bigrams[context]:
            word_count = self._bigrams[context][word]
        else:
            word_count = 0
        val = (word_count + 1)/(total_count + self._word_count)
        return log(val)

    def add_train(self, sentence):
        """
        Add the counts associated with a sentence.
        """

        # You'll need to complete this function, but here's a line of code that
        # will hopefully get you started.
        for context, word in bigrams(list(self.tokenize_and_censor(sentence))):
            None
            # ---------------------------------------
            assert word in self._vocab, "%s not in vocab" % word
            assert context in self._vocab, "%s not in vocab" % context
            if context in self._bigrams:
                if word in self._bigrams[context]:
                    self._bigrams[context][word] = self._bigrams[context][word] + 1
                else:
                    self._bigrams[context][word] = 1
            else:
                self._bigrams[context] = {word: 1}

    def log_likelihood(self, sentence):
        """
        Compute the log likelihood of a sentence, divided by the number of
        tokens in the sentence.
        """
        # you need to do stuff bitch
        #sent = tokenize(sentence)
        sent = self.tokenize_and_censor(sentence)
        prob = 0
        first = True
        total = 0
        for word in sent:
            total = total + 1
            if first:
                first = False
            else:
                prob = prob + self.laplace(prev_word, word)
            prev_word = word
        return prob/total


if __name__ == "__main__":
    dem_lm = BigramLanguageModel()
    rep_lm = BigramLanguageModel()
    '''dem_lm.train_seen("the")
    dem_lm.train_seen("nation")
    dem_lm.finalize()
    dem_lm.add_train("the nation")
    dem_lm.add_train("nation")
    dem_lm.laplace("the","nation")
    sent = "hi my name is jessica and i am happy jessica is happy jessica is awesome"
    for word in tokenize(sent):
        dem_lm.train_seen(word)
    dem_lm.finalize()
    dem_lm.add_train(sent)
    new_sent = "jessica is awesome"
    print(dem_lm.laplace("jessica", "is"))
    print(dem_lm.log_likelihood(new_sent))'''

    for target, pres, name in [(dem_lm, kDEM, "D"), (rep_lm, kREP, "R")]:
        for sent in sentences_from_zipfile("../data/state_union.zip", pres):
            for ww in tokenize(sent):
                target.train_seen(ww)
                
        print("Done looking at %s words, finalizing vocabulary" % name)
        target.finalize()
        
        for sent in sentences_from_zipfile("../data/state_union.zip", pres):
            target.add_train(sent)
    
        print("Trained language model for %s" % name)

    with open("../data/2016-obama.txt") as infile:
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
            
            
