from os import walk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class InvertedIndex:
    def __init__(self):
        file_contents, self.file_names = self._read()
        searchable_file_contents = [self._parse(document) for document in file_contents]
        self.keywords = self._extract(searchable_file_contents)
        self.index = self._invert(searchable_file_contents, self.keywords)

    def search(self, keyword) -> tuple[str]:
        if keyword not in self.keywords:
            return tuple()
        ids = self.index[keyword]
        return tuple(self.file_names[doc_id] for doc_id in ids)

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
    def _parse(document: str) -> list[str]:
        # lowercase
        document = document.lower()
        # without punctuation
        for punctuation in "!()-[]{};:, <>./?@#$%^&*_~'\"\\":
            document = document.replace(punctuation, " ")
        # tokens
        tokens = word_tokenize(document)
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
    def _invert(documents: list[list[str]], keywords: set[str]) -> dict[str, tuple[int]]:
        return {
            keyword: tuple(
                i for i, document in enumerate(documents) if (keyword in document)
            )
            for keyword in keywords
        }


if __name__ == "__main__":
    index = InvertedIndex()
    print("chapter", index.search("chapter"))
    print("even", index.search("even"))
    print("xi", index.search("xi"))
    print("expostulation", index.search("expostulation"))
