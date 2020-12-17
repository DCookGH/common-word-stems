import unittest
from StemFrequency import StemFrequency


class TestStemFrequency(unittest.TestCase):
    def test_tokenize_text(self):
        check = TestStemFrequency._assert_msg
        sf = StemFrequency()
        text = "a ab a-b aa-bb aa'bb --ab ab-- 'word word' \"word word\" ab\nab\tab 1 1234567890 \\ "\
               "end. end! end? * $ % # a\u0144b 1ab ab1 a1b dash--dash abc's out-of-the-way "\
               " _a_ b_c d__e __f__ _g h_"
        expected = ["a", "ab", "ab", "aabb", "aa'bb", "ab", "ab", "word", "word", "word", "word", "ab", "ab", "ab",
                    "end", "end", "end", "a\u0144b", "ab", "ab", "ab", "dash", "dash", "abc's", "outoftheway",
                    "a", "bc", "de", "f", "g", "h"]
        check(sf.tokenize_text(text), expected)
        text = "ours\n\tourselves\nout\nover\nown\nsame\nshan't\nshe\nshe'd\nshe'll"
        expected = ["ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll"]
        check(sf.tokenize_text(text), expected)
        check(sf.tokenize_text(""), [])

    def test_find_frequency(self):
        check = TestStemFrequency._assert_msg
        sf = StemFrequency()
        words = ["a", "b", "a", "c", "ab", "aa", "a-b", "a'b", "ab", "ab", "a-b", "a'b"]
        expected = {"a": 2, "b": 1, "c": 1, "ab": 3, "aa": 1, "a-b": 2, "a'b": 2}
        check(sf.find_frequency(words), expected)
        check(sf.find_frequency([]), {})

    def test_remove_stopwords(self):
        check = TestStemFrequency._assert_msg
        stopwords = ["a", "b", "ab", "xyz", "ab-cd", "aa'b"]
        sf = StemFrequency(stopwords=stopwords)
        words = {"c": 1, "a": 2, "abc": 3, "xy": 4, "wxyz": 5, "ab-cd": 6, "aa'b": 7, "xyz": 8}
        expected = {"c": 1, "abc": 3, "xy": 4, "wxyz": 5}
        check(sf.remove_stopwords(words), expected)
        check(sf.remove_stopwords({}), {})
        check(sf.remove_stopwords({"c": 1, "cd": 2}), {"c": 1, "cd": 2})



    def test_stem_and_consolidate(self):
        check = TestStemFrequency._assert_msg
        sf = StemFrequency()
        check(sf.stem_and_consolidate({"a": 5}), {"a": 5})
        check(sf.stem_and_consolidate({}), {})
        check(sf.stem_and_consolidate({"a": 5}), {"a": 5})
        check(sf.stem_and_consolidate({"nature's": 5}), {"nature'": 5})
        check(sf.stem_and_consolidate({"nature's": 5}, remove_apostrophes=True), {"natur": 5})
        check(sf.stem_and_consolidate({"natures": 5}), {"natur": 5})
        check(sf.stem_and_consolidate({"nature": 5}), {"natur": 5})
        check(sf.stem_and_consolidate({"can't": 5}), {"can't": 5})
        check(sf.stem_and_consolidate({"can't": 5}, remove_apostrophes=True), {"cant": 5})
        check(sf.stem_and_consolidate({"cant": 5}), {"cant": 5})
        check(sf.stem_and_consolidate({"dinah'll": 5}), {"dinah'l": 5})
        check(sf.stem_and_consolidate({"dinah'll": 5}, remove_apostrophes=True), {"dinahl": 5})
        check(sf.stem_and_consolidate({"dinahll": 5}), {"dinahl": 5})
        check(sf.stem_and_consolidate({"dinah": 5}), {"dinah": 5})
        check(sf.stem_and_consolidate({"to-day": 5}), {"to-dai": 5})
        check(sf.stem_and_consolidate({"today": 5}), {"todai": 5})
        check(sf.stem_and_consolidate({"self-evident": 5}), {"self-evid": 5})
        check(sf.stem_and_consolidate({"selfevident": 5}), {"selfevid": 5})
        check(sf.stem_and_consolidate({"dogs": 5}), {"dog": 5})
        check(sf.stem_and_consolidate({"blindly": 5}), {"blindli": 5})
        check(sf.stem_and_consolidate({"running": 5}), {"run": 5})
        check(sf.stem_and_consolidate({"dog": 3, "a": 2, "dogs": 4}), {"dog": 7, "a": 2})
        check(sf.stem_and_consolidate({"dog": 3, "blind": 2, "dogs": 4, "blinds": 5, "blinding": 6}),
              {"dog": 7, "blind": 13})

    def test_most_common(self):
        freq = {"c": 1, "b": 2, "a": 1, "d": 3, "e": 1, "f": 5, "g": 3}
        check = TestStemFrequency._assert_msg
        sf = StemFrequency()
        check(sf.most_common({}, 0), [])
        check(sf.most_common(freq, 0), [])
        check(sf.most_common(freq, 1), [("f", 5)])
        check(sf.most_common(freq, 2), [("f", 5), ("d", 3)])
        check(sf.most_common(freq, 3), [("f", 5), ("d", 3), ("g", 3)])
        check(sf.most_common(freq, 4), [("f", 5), ("d", 3), ("g", 3), ("b", 2)])
        check(sf.most_common(freq, 5), [("f", 5), ("d", 3), ("g", 3), ("b", 2), ("a", 1)])
        check(sf.most_common(freq, 8), [("f", 5), ("d", 3), ("g", 3), ("b", 2), ("a", 1), ("c", 1), ("e", 1)])
        check(sf.most_common(freq, 100), [("f", 5), ("d", 3), ("g", 3), ("b", 2), ("a", 1), ("c", 1), ("e", 1)])

    @staticmethod
    def _assert_msg(actual, expected):
        assert actual == expected, "Expected {}, but got {}".format(expected, actual)


if __name__ == '__main__':
    unittest.main()
