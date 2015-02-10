IDD3
====

IDD3 (*Propositional Idea Density from Dependency Trees*) is a Python library that can extract propositions from a sentence, given its dependency tree. Propositions are extracted according to Chand et al.'s rubric [1].

Installation
------------

To install IDD3 on your system, run can run:

```
$ git clone https://github.com/andrecunha/idd3.git
$ cd idd3
$ python setup.py install
```

You might want to install IDD3 inside a virtualenv.

How to run the example file
---------------------------

IDD3 ships with a `run.py` file, that illustrates how the library can be accessed. This file can be used to easily analyze sentences and see the system's output. You can use this file to analyze either a raw sentence, or its dependency tree, stored in a CoNLL file. In order to analyze raw sentences, follow these steps:

1. `run.py` uses the Stanford Parser to extract the dependency tree. Download the latest version of it at http://nlp.stanford.edu/software/lex-parser.shtml#Download, and extract it where you want.
2. Change the variable `stanford_path` in `run.py` to point to the path where you extracted the parser in the previous step (the default value is `~/Develop/stanford_tools/`).
3. Place the sentences you want to analyze in a file, let's say `input.txt`, one sentence per line.
4. Run IDD3 as `python run.py input.txt`

If you have a CoNLL-X file, say `input.conll`, that already has the dependency trees for the sentences you want IDD3 to analyze, you can just run `python run.py input.conll`.

References
----------

[1]  V. Chand, K. Baynes, L. Bonnici, and S. T. Farias, *Analysis of Idea Density (AID): A Manual*, University of California at Davis, 2010. Available at http://mindbrain.ucdavis.edu/labs/Baynes/AIDManual.ChandBaynesBonniciFarias.1.26.10.pdf.
