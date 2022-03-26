import json
from math import ceil, log
from typing import Callable, Optional

from inverted_index import InvertedIndex

PARAM_s = 1
PARAM_L = 1


class SSE:
    # Setup algorithm
    def __init__(self, debug: bool = False):
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
        first_level = ceil(log(self.N))
        p = ceil(first_level / PARAM_s)
        self.levels = [first_level - p * i for i in range(PARAM_s)]
        if PARAM_L > 1:
            self.levels.insert(0, 0)
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
            level_index: int = self.levels[upper_level_index]
            # 10
            large_chunk_size = 2**level_index
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
                for bucket_index in range(self.number_of_buckets(level_index)):
                    # For small bucket
                    if (
                        self.small_bucket_size != 0
                        and bucket_index == self.number_of_buckets(level_index) - 1
                    ):
                        if (
                            self.small_bucket_size(level_index)
                            - len(self.arrays[level_index][-1])
                            <= large_chunk_size
                        ):
                            first_empty_bucket_index = bucket_index
                            break
                    # For large buckets
                    else:
                        if (
                            self.large_bucket_size(level_index)
                            - len(self.arrays[level_index][bucket_index])
                            <= large_chunk_size
                        ):
                            first_empty_bucket_index = bucket_index
                            break
                # 15
                if first_empty_bucket_index is not None:
                    self.arrays[level_index][first_empty_bucket_index].append(
                        documents_containing_keyword[
                            count * large_chunk_size : (count + 1) * large_chunk_size
                        ]
                    )
                else:
                    raise IndexError("Chunk did not fit in any bucket")
                # 16
                # TODO: Encrypt key & value before adding to table
                key = keyword
                value = (level_index, first_empty_bucket_index)
                self.hash_table[key] = value
            # 11 - 16 for last (small) chunk
            # 11 - 13
            if small_chunk_size != 0:
                # 14
                first_empty_bucket_index: Optional[int] = None
                for bucket_index in range(self.number_of_buckets(level_index)):
                    # For small bucket
                    if (
                        self.small_bucket_size != 0
                        and bucket_index == self.number_of_buckets(level_index) - 1
                    ):
                        if (
                            self.small_bucket_size(level_index)
                            - len(self.arrays[level_index][-1])
                            <= small_chunk_size
                        ):
                            first_empty_bucket_index = bucket_index
                            break
                    # For large buckets
                    else:
                        if (
                            self.large_bucket_size(level_index)
                            - len(self.arrays[level_index][bucket_index])
                            <= small_chunk_size
                        ):
                            first_empty_bucket_index = bucket_index
                            break
                # 15
                if first_empty_bucket_index is not None:
                    self.arrays[level_index][first_empty_bucket_index].append(
                        documents_containing_keyword[-small_chunk_size:]
                    )
                else:
                    raise IndexError("Chunk did not fit in any bucket")

                # 16
                # TODO: Encrypt key & value before adding to table
                key = keyword
                value = (level_index, first_empty_bucket_index)
                self.hash_table[key] = value
            return

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

    def search(self):
        raise NotImplementedError()


if __name__ == "__main__":
    raise NotImplementedError(
        "This module is not intended to be run directly\n"
        "If you wish to use it, import `InvertedIndex`\n"
        "If you wish to test it, run `test_inverted_index.py`"
    )