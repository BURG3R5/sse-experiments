import unittest

from inverted_index import InvertedIndex


class TestInvertedIndex(unittest.TestCase):
    index: InvertedIndex

    @classmethod
    def setUpClass(cls):
        cls.index = InvertedIndex()

    def test_keyword_search(self):
        self.assertEqual(
            self.index.search("chapter"),
            {"d.txt", "a.txt", "b.txt"},
        )
        self.assertEqual(
            self.index.search("even"),
            {"d.txt", "a.txt", "b.txt", "f.txt"},
        )
        self.assertEqual(self.index.search("xi"), {"a.txt"})
        self.assertEqual(self.index.search("expostulation"), {"d.txt"})

    def test_phrase_search(self):
        self.assertEqual(self.index.search("chapter xix"), {"a.txt"})
        self.assertEqual(
            self.index.search("even smaller"),
            {"b.txt", "f.txt"},
        )


if __name__ == "__main__":
    unittest.main()
