from os import walk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class InvertedIndex:
    def __init__(self):
        file_contents, self.file_names = self._read()
        searchable_file_contents = [self._parse(document) for document in file_contents]
        self.keywords = self._extract(searchable_file_contents)
        self.index = self._invert(searchable_file_contents, self.keywords)

    def search(self, query: str) -> set[str]:
        terms: list[str] = self._parse(query)
        if len(terms) == 1:
            keyword: str = terms[0]
            if keyword not in self.keywords:
                return set()
            ids = self.index[keyword]
            return set(self.file_names[doc_id] for doc_id in ids)
        else:
            results: set[str] = set(self.file_names)
            for keyword in terms:
                results = results.intersection(self.search(keyword))
            return results

    @staticmethod
    def _read() -> tuple[list[str], list[str]]:
        documents: list[str] = []
        # Get files in `documents/` directory
        (_, _, file_names) = next(walk("documents"))

        for file_name in file_names:
            # Open and read each file, line-wise
            with open("documents/" + file_name, encoding="UTF-8") as file:
                documents += [""]
                for line in file:
                    documents[-1] += line
        return documents, file_names

    @staticmethod
    def _parse(string: str) -> list[str]:
        # lowercase
        string = string.lower()
        # without punctuation
        for punctuation in "!()-[]{};:, <>./?@#$%^&*_~'\"\\":
            string = string.replace(punctuation, " ")
        # tokens
        tokens = word_tokenize(string)
        # without stopwords
        tokens = [token for token in tokens if token not in stopwords.words()]
        return tokens

    @staticmethod
    def _extract(documents: list[list[str]]) -> set[str]:
        keywords: set[str] = set()
        for document in documents:
            keywords = keywords.union(set(document))
        return keywords

    @staticmethod
    def _invert(
        documents: list[list[str]],
        keywords: set[str],
    ) -> dict[str, tuple[int]]:
        return {
            keyword: tuple(
                i for i, document in enumerate(documents) if (keyword in document)
            )
            for keyword in keywords
        }


if __name__ == "__main__":
    raise NotImplementedError(
        "This module is not intended to be run directly\n"
        "If you wish to use it, import `InvertedIndex`\n"
        "If you wish to test it, run `test_inverted_index.py`"
    )
