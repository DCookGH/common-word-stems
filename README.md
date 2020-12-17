# common-word-stems

This repository contains a program to read a text file and print out the 20 most commonly occuring word stems, not including words from a set of stopwords.
The code is written in python.

To run the program, make sure all the files are in the same directory, and in that directory, run either of the following commands, depending on which file you want to read the text of:

`python StemFrequency.py Text1.txt`

`python StemFrequency.py Text2.txt`

You can even run it on another text file of your choosing by passing in the path to the file instead of "Text1.txt" or "Text2.txt"

There are 3 source code files:
* StemFreqency.py - This is the main logic for the program.
* PorterStemmer.py - This is the Porter Stemmer algorithm.
  * It is a nearly exact copy of the code provided at https://tartarus.org/martin/PorterStemmer/python.txt with the syntaxt of one line changed to allow it to run without crashing.
* TestStemFreqency.py - This contains the unit tests.
  * You can run them from the command line with: `python TestStemFrequency.py`

## Brief notes:
The program does the following, in order:
* Read the text file into a string
* Tokenize the text into a list of words
  * During this process is when non-alphabetic characters are removed, except for apostrophes. (see detailed notes below for explanation)
  * Letters are also converted to lower-case.
* Count the frequency of each word, creating a dictionary that maps each distinct word to its frequency
* Read the stopwords.txt file into a list of stopwords, and remove those words from the frequency dictionary
* Run the PorterStemmer on each word in the frequency dictionary, summing up the frequencies of words that are stemmed to the same stem, and creating a dictionary of stems to their frequencies
  * For example, `{"dogs": 2, "dog": 3}` would become `{"dog": 5}`
  * Also, apostrophes are removed here, just before the stemming is done. (see detailed notes below for explanation)
* Find the 20 most common stems, in descending order
  * I was faced with another choice here: how to order stems with the same frequency. I could either keep them in the same order (which in this case was the order that they were first found in the text), or choose some secondary order, such as alphabetical. I wrote both into the function, but had it default to keeping the original order.
* Print out the 20 most common stems
  * I print the frequencies with the stems, although the specification doesn't explicitly demand it. It would be a trivial change to print just the stems.

I switched up the order of the operations listed in the specification. Instead of following this order:
* remove stop words
* remove non-alphabetic text
* stem words
* compute frequency

I followed this order:
* remove non-alphabetic text (not including apostrophes)
* compute frequency
* remove stopwords
* remove apostrophes
* stem words (and roll-up frequencies)

This results in the same output, but because the stopword and stemming removal comes after computing the frequency, those operations only have to be done once per unique word, which allows for better performance.

As noted above, for stems of the same frequency, I kept them in the order they first appeared in the text.

## Output:
For reference, the output of the program for the two files is as follows:

For Text1.txt:
```
us (11)
peopl (10)
right (10)
govern (10)
law (9)
state (9)
power (8)
time (6)
among (5)
declar (5)
establish (5)
refus (5)
form (4)
abolish (4)
new (4)
coloni (4)
assent (4)
larg (4)
legislatur (4)
legisl (4)
```

For Text2.txt:
```
said (462)
alic (402)
littl (128)
on (105)
look (104)
like (97)
know (92)
went (83)
thing (79)
go (77)
thought (76)
queen (76)
time (74)
sai (71)
get (68)
see (68)
think (64)
king (64)
turtl (61)
well (60)
```

## Additional detailed notes that not everyone may care about:
### Stopwords file:
I noticed that "ourselves" had a tab before it, hence the pattern matching to split it instead of just doing a string split on '\n'.

### Removal of non-alphabetic characters and tokenization:
The order of when you remove non-alphabetic characters is important, as to where it occurs in relation to the tokenization, stopword removal, and stemming.
In most cases, the pattern-matching I use to tokenize the text also removes non-alphabetic characters. There are a few characters that required special handling, as follows.

#### Apostrophes:
The stopwords contained contractions, so apostropies couldn't be removed from the text representation until after the stopwords were removed. Most contractions were removed by the stopwords themselves, but they didn't contain contractions to arbitrary words or proper nouns. For instance, Text2.txt contained "Dinah'll". The stemmer handling is not apostrophe-independent. For instance, the plural "natures" stems to "natur", but the possessive "nature's" stems to "nature'". Since these words should be considered the same stem, and since we eventually have to remove non-alphabetic characters per the spec, I decided to remove the apostrophe before doing the stemming. The drawback is that arbitrary contractions like "Dinah" and "Dinah'll" will not counted as two "Dinah" stems, but that is acceptible, if not desireable. (As a side note, apostrophes not falling within a word are removed by the tokenization pattern, e.g. "\'word", or "word\'")

#### Hyphens:
Some words are hyphenated, but there are varying degrees to which the parts hyphenated by seperate parts can be considered independent of each other. The stopwords file doesn't contain any hyphenated words, so that gives us some freedom. Text2.txt contains all of the following words:
* to-day
* today
* waistcoat- pocket
* waistcoat-pocket
* out-of-the-way

On one extreme you have "to-day", which clearly has the same stem as "today". On the other extreme, you have "out-of-the-way", which might be considered a string of four stems, rather than just one stem like "outoftheway". Since it seems closer to a single concept than "to-day" seems like it could be two, I errored on the side of treating hyphenated words as inseperable.

However, there is still the problem of dashes, which could be represented as two hyphens (and in fact is in Text2.txt). Dashes always seperate words, so you can't just remove all hyphens before tokenizing.

Therefore, I consider single hyphens inside words a non-separating in the pattern-matching during tokenization, but then I remove the hyphens from the tokens immediately after.
I don't do any special handling to account for potential typos like "waistcoat- pocket". Those are just considered two words.

#### Numbers:
I remove these before tokenization. This would matter if there was a word containing a number, such as "passw0rd", in which case it would be considered one word ("passwrd"), instead of two ("passw", "rd"). There is nothing like this in any of the text files.

#### Underscores:
I remove these before tokenization, like numbers. They don't make a difference in these text files. Text2.txt contains "_I_", but there are no underscores that fall between two alphabetic characters.
