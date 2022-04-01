import json
from math import ceil, log
from typing import Callable, Optional

from src.inverted_index import InvertedIndex
from utils.parse_utils import ParseUtils

PARAM_s = 4
PARAM_L = 1


class SSE:
    # Setup algorithm
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.inverted_index = InvertedIndex(debug=True)  # 0
        # TODO: Get keys  # 1
        self._calculate_params()  # 2
        self.hash_table, self.arrays = self._init_arrays()  # 3 - 7
        self._fill_arrays_and_hash_table()  # 8 - 16
        # TODO: Pad hash table  # 17
        # TODO: Randomize elements in arrays and encrypt them again  # 18 - 21
        if debug:
            self._store_hash_table_and_arrays()  # 22 - 23

    # Setup algorithm sub-methods
    def _calculate_params(self):
        self.N = sum(len(arr) for arr in self.inverted_index.index.values())
        first_level = ceil(log(self.N, 2))
        p = ceil(first_level / PARAM_s)
        self.levels = [first_level - p * i for i in range(PARAM_s - 1, -1, -1)]
        if PARAM_L > 1:
            self.levels.insert(0, 0)
        if self.debug:
            print(f"N: {self.N}\n" f"levels: {self.levels}")
        # Some utility shortcuts
        self.array_size: Callable[[int], int] = lambda i: 2 * (self.N + 2**i)
        self.large_bucket_size: Callable[[int], int] = lambda i: 2 ** (i + 1)
        self.small_bucket_size: Callable[[int], int] = lambda i: (
            2 * (self.N + 2**i)
        ) % (2 ** (i + 1))
        self.number_of_large_buckets: Callable[[int], int] = lambda i: (
            2 * (self.N + 2**i)
        ) // (2 ** (i + 1))
        self.number_of_buckets: Callable[
            [int], int
        ] = lambda i: self.number_of_large_buckets(i) + (self.small_bucket_size(i) != 0)

    def _init_arrays(self) -> tuple[dict[str, tuple[int, int]], list[list[list]]]:
        return {}, [
            [[] for __ in range(self.number_of_buckets(i))] for i in self.levels
        ]

    def _fill_arrays_and_hash_table(self):
        # TODO: Randomize order of filling
        # 8
        for keyword in self.inverted_index.keywords:
            # 9
            documents_containing_keyword = self.inverted_index.index[keyword]
            number_of_documents_containing_keyword = len(documents_containing_keyword)
            bound = log(len(documents_containing_keyword) / PARAM_L, 2)
            upper_level_index = min(
                index for index, level in enumerate(self.levels) if level >= bound
            )
            level: int = self.levels[upper_level_index]
            # 10
            large_chunk_size = 2**level
            number_of_large_chunks, small_chunk_size = divmod(
                number_of_documents_containing_keyword,
                large_chunk_size,
            )
            # 11 - 16 for large chunks
            # 11 - 13
            for count in range(number_of_large_chunks):
                # TODO: Randomize selection of buckets
                # 14
                first_empty_bucket_index: Optional[int] = None
                for bucket_index in range(self.number_of_buckets(level)):
                    # For small bucket
                    if (
                        self.small_bucket_size(level) != 0
                        and bucket_index == self.number_of_buckets(level) - 1
                    ):
                        level_index = self.levels.index(level)
                        if (
                            self.small_bucket_size(level)
                            - len(self.arrays[level_index][-1])
                            >= large_chunk_size
                        ):
                            first_empty_bucket_index = bucket_index
                            break
                    # For large buckets
                    else:
                        level_index = self.levels.index(level)
                        if (
                            self.large_bucket_size(level)
                            - len(self.arrays[level_index][bucket_index])
                            >= large_chunk_size
                        ):
                            first_empty_bucket_index = bucket_index
                            break
                # 15
                if first_empty_bucket_index is not None:
                    level_index = self.levels.index(level)
                    self.arrays[level_index][first_empty_bucket_index] += [
                        (doc, keyword)
                        for doc in documents_containing_keyword[
                            count * large_chunk_size : (count + 1) * large_chunk_size
                        ]
                    ]
                else:
                    raise IndexError(
                        "Chunk did not fit in any bucket\n"
                        f"Chunk size: {small_chunk_size}, "
                        f"Level: {level}, "
                        f"Bucket sizes: ({self.large_bucket_size(level)} "
                        f"& {self.small_bucket_size(level)})"
                    )
                # 16
                # TODO: Encrypt key & value before adding to table
                key = keyword
                value = (level, first_empty_bucket_index)
                self.hash_table[key] = value
            # 11 - 16 for last (small) chunk
            # 11 - 13
            if small_chunk_size != 0:
                # 14
                first_empty_bucket_index: Optional[int] = None
                for bucket_index in range(self.number_of_buckets(level)):
                    # For small bucket
                    if (
                        self.small_bucket_size(level) != 0
                        and bucket_index == self.number_of_buckets(level) - 1
                    ):
                        level_index = self.levels.index(level)
                        if (
                            self.small_bucket_size(level)
                            - len(self.arrays[level_index][-1])
                            >= small_chunk_size
                        ):
                            first_empty_bucket_index = bucket_index
                            break
                    # For large buckets
                    else:
                        level_index = self.levels.index(level)
                        if (
                            self.large_bucket_size(level)
                            - len(self.arrays[level_index][bucket_index])
                            >= small_chunk_size
                        ):
                            first_empty_bucket_index = bucket_index
                            break
                # 15
                level_index = self.levels.index(level)
                if first_empty_bucket_index is not None:
                    self.arrays[level_index][first_empty_bucket_index] += [
                        (doc, keyword)
                        for doc in documents_containing_keyword[-small_chunk_size:]
                    ]
                else:
                    raise IndexError(
                        "Chunk did not fit in any bucket\n"
                        f"Chunk size: {small_chunk_size}, "
                        f"Level: {level}, "
                        f"Bucket sizes: ({self.large_bucket_size(level)} "
                        f"& {self.small_bucket_size(level)})"
                    )

                # 16
                # TODO: Encrypt key & value before adding to table
                key = keyword
                value = (level, first_empty_bucket_index)
                self.hash_table[key] = value

    def _store_hash_table_and_arrays(self):
        with open("documents/arrays.json", mode="w", encoding="utf-8") as file:
            json.dump(self.arrays, file)
        with open("documents/hash_table.json", mode="w", encoding="utf-8") as file:
            json.dump(self.hash_table, file)

    @staticmethod
    def _chunks(array: list, n: int) -> list:
        """
        Yield successive n-sized chunks from a list.
        """
        n = max(1, n)
        return [array[i : i + n] for i in range(0, len(array), n)]

    def keygen(self):
        raise NotImplementedError()

    def token(self):
        raise NotImplementedError()

    # Search algorithm
    def search(self, query: str) -> set:
        terms: list[str] = ParseUtils.parse(query)
        if len(terms) == 1:
            result = []
            # TODO: Will have to modify this if and when arrays and hash_table are encrypted.
            # 3 - 4
            try:
                location = self.hash_table[query]
                try:
                    level, bucket_index = location
                    level_index = self.levels.index(level)
                    bucket = self.arrays[level_index][bucket_index]
                    result += [entry[0] for entry in bucket if entry[1] == query]
                except TypeError:
                    # If `location` is not of the correct form, the data is incorrectly stored.
                    raise TypeError(
                        f"`location` is not of the correct type.\n"
                        f"Expected: tuple[int, int]\n"
                        f"Got: {type(location)}"
                    )
            except KeyError:
                # If `query` is not found in `hash_table`, just return an empty set.
                pass
            return set(result)
        else:
            results: set[str] = self.search(terms[0])
            for keyword in terms[1:]:
                results = results.intersection(self.search(keyword))
            return results


if __name__ == "__main__":
    raise NotImplementedError(
        "This module is not intended to be run directly\n"
        "* If you wish to use it, import `SSE`\n"
        "* If you wish to test it, run `test_sse.py`"
    )
