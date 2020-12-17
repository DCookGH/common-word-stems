import re
import heapq
import sys

from PorterStemmer import PorterStemmer


class StemFrequency:
    TOKENIZER_PATTERN = r'\w+(?:[-\']\w+)*'

    def __init__(self, stemmer=None, stopwords_file='stopwords.txt', stopwords=None):
        self.stemmer = stemmer if stemmer is not None else PorterStemmer()
        self.stopwords = stopwords
        if stopwords is None:
            with open(stopwords_file, 'r') as f:
                raw = f.read()
            self.stopwords = re.findall(StemFrequency.TOKENIZER_PATTERN, raw)

    def tokenize_text(self, text):
        """
        Turns a string of text into a list of words.
        Punctuation, numbers, and special characters are removed, but words may still contain apostrophes.
        Removes hyphens after tokenizing, so that multiple hyphens define word boundaries, but single hyphens do not.
        :param text: the text to tokenize
        :return: a list of words
        """
        tokens = re.findall(StemFrequency.TOKENIZER_PATTERN, re.sub(r'[0-9_]+', '', text.lower()))
        return list(map(lambda x: x.replace('-', ''), tokens))

    def find_frequency(self, words):
        """
        Takes a list of words and makes a dictionary mapping unique words to their frequency in the original list
        :param words: a list of words
        :return: a dictionary where the keys are words, and the values are frequencies
        """
        frequency = {}
        for word in words:
            if word not in frequency:
                frequency[word] = 1
            else:
                frequency[word] += 1
        return frequency

    def remove_stopwords(self, words):
        """
        Removes blacklisted keys from a dictionary
        :param words: A dictionary where the keys are to be compared against a blacklist
        :param stopwords: A list of keys to remove from a dictionary
        :return: a dictionary with the blacklisted keys removed
        """
        for stopword in self.stopwords:
            if stopword in words:
                words.pop(stopword)
        return words

    def stem_and_consolidate(self, frequencies, remove_apostrophes=False):
        """
        Takes a word-to-frequency dictionary and stems the words, summing the frequencies of words that map to the same stem
        Also, apostrophes are removed first.
        :param frequencies: a dictionary of words to frequencies
        :param remove_apostrophes: if True, then remove the apostrophes from words before stemming
        :return: a dictionary of stems to frequencies
        """
        consolidated = {}
        for word, frequency in frequencies.items():
            if remove_apostrophes:
                word = word.replace("'", "")
            stemmed = self.stemmer.stem(word, 0, len(word) - 1)
            if stemmed in consolidated:
                consolidated[stemmed] += frequency
            else:
                consolidated[stemmed] = frequency
        return consolidated

    def most_common(self, frequencies, count):
        """
        Given a dictionary of strings to their frequency, finds the most common strings in order of descending
        frequency, then ascending alphabetical
        :param frequencies: a dictionary of strings to their frequency
        :param count: the number of strings to return
        :return: a list of tuples of the most common strings in descending order of frequency: (stem, frequency)
        """
        return heapq.nsmallest(count, frequencies.items(), key=lambda x: (-x[1], x[0]))

    def find_common_stems(self, file_name, count=20):
        """
        Finds the most common word stems in a text file, excluding certain stopwords
        :param file_name: the name of the text file to find the common word stems in
        :param count: the number of stems to find
        :return: a list of the most common stems in the file, in descending order of frequency
        """
        with open(file_name, 'r') as f:
            raw = f.read()
        words = self.tokenize_text(raw)
        word_counts = self.find_frequency(words)
        cleaned_counts = self.remove_stopwords(word_counts)
        stem_counts = self.stem_and_consolidate(cleaned_counts, remove_apostrophes=True)
        return self.most_common(stem_counts, count)


if __name__ == '__main__':
    # get filepath if passed-in
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'Text2.txt'
    stem_frequency = StemFrequency()
    for stem in stem_frequency.find_common_stems(filepath, 20):
        print("{} ({})".format(stem[0], stem[1]))
