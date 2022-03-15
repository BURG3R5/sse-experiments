import unittest

from inverted_index import InvertedIndex


class TestInvertedIndex(unittest.TestCase):
    index: InvertedIndex

    @classmethod
    def setUpClass(cls):
        cls.index = InvertedIndex()

    def test_keyword_search(self):
        self.assertEqual(
            {"$2qtvxQyjKj9Z4PftGuPNX1G-gBrYCDiXkBGuQNt6TAk"},
            self.index.search("presumably"),
        )
        self.assertEqual(
            {
                "$DjYYT7h9Tc0BD23r7HXE0bl8IzXtbr24Yp6Q1fFTubw",
                "$EoHmLc15G6G834SRAT7k-mFFapLcWCoJXr1iUX6zWdA",
            },
            self.index.search("employee"),
        )
        self.assertEqual(
            self.index.search("discord"),
            {
                "$3aiTubd-TUMdw4WNpBI4qTXn8WhM0v7HEfxJILW0vrg",
                "$xmPxf676bStqnUwCrM0L877v4kr3CRN5WaFPuzS1GI4",
                "$5QypiKAFPA-GnLRvmm6boreYzYJ3pdzD702_28xAhn8",
                "$ajBj2nDQIFh3Q0VYM6N1Re_C5zQklVCsGwAOzCVTlI4",
            },
        )

    def test_phrase_search(self):
        self.assertEqual(
            self.index.search("mentors stretch"),
            {"$4gwwUIaNRhdfcNx2auecdFDxY_clGoLRiiLsWwf0epU"},
        )
        self.assertEqual(
            self.index.search("late reply"),
            {"$H5GJ-YyrAvWGMYmTwgB0JUVAE0_bbIP6xATOszrxJHg"},
        )


if __name__ == "__main__":
    unittest.main()
