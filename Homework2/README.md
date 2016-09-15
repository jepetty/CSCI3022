
Estimating Distribution Parameters
===============

Overview
---------------

This program will be autograded.  That means that it's important to
not change function names and to not add additional functionality that
may improve the program but produce different results.  Make sure that
your unit tests pass.  This what a successful set of unit tests will
look like:

    $ python3 tests.py
    .....
    ----------------------------------------------------------------------
    Ran 5 tests in 0.002s
    
    OK

Districts (10 points)
----------------------------

In the US, our legislature is made up of representatives of individual
*districts* (unlike proportional representation systems).  Your task
is to characterize districts in "Red" Republican states vs. districts
in "Blue" Democratic states.

First, you'll need to extract the Republican share of the vote in a
district.  Then, you will need to compute the parameters of a Gaussian
distribution, then compute the probability of an observation given
those parameters.

You will need to implement the following functions:
* ml_mean
* ml_variance
* log_probability
* republican_share

After you've done that, the main function will then report for each of
Colorado's district whether it looks more like a red state or a blue state.

Words Presidents Use (20 points)
-------------------------------

Each year, the president of the United States is required to make a
speech to congress describing the "State of the Union".  We are going
to create a simple *bigram language model* with *add one (Laplace)*
smoothing.  Your task is to characterize Republican vs. Democrat
presidents based on their speech.

To do this, you'll need to implement the following functions:
* train_seen
* generate
* laplace
* add_train

WARNING: Writing a unit test for generation is tricky (without
creating a testing stub for the random number generator), so make sure
you are dillegent in making sure this works correctly.

Writeup (10 points)
-----------------------

Finally, include a brief plain-text file (not PDF, not Word, just a
plain ASCII text file) that:
* Describes your approach
* Describes whether Colorado's congression districts look more like
  the congressional districts of states that Obama won or that Romeny
  won
* Plot a
  [histogram](http://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html)
  of both the Obama and Romney states.  Is it resonable to assume that
  these are a normal distribution?
* Gives an interesting example of a *word* that Obama said that no
  previous president said
* Gives an interesting example of a *bigram* that Obama said that no
  previous president said
* Generates a random sentence from a Republican and a Democrat.

Submitting Your Code
-----------------------

You'll need to submit your assignment (lm.py, districts.py,
histogram.png, and writeup.txt) on Moodle as an upload.
