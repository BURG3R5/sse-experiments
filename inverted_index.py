import json
from os import walk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from utils import ReadUtils


class InvertedIndex:
    def __init__(self):
        self.documents = ReadUtils.read_messages_element()
        searchable_documents: dict[str, list[str]] = {
            document_id: self._parse(document_content)
            for document_id, document_content in self.documents.items()
        }
        self.keywords = self._extract(searchable_documents)
        self.index = self._invert(searchable_documents, self.keywords)
        # TODO: This is temporary vvvvvvvvvv
        with open("documents/index.json", mode="w", encoding="utf-8") as file:
            json.dump(self.index, file)
        # TODO: This is temporary ^^^^^^^^^

    def search(self, query: str) -> set[str]:
        terms: list[str] = self._parse(query)
        if len(terms) == 1:
            keyword: str = terms[0]
            if keyword not in self.keywords:
                return set()
            ids = self.index[keyword]
            return set(ids)
        else:
            results: set[str] = set(self.documents.keys())
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
    def _extract(documents: dict[str, list[str]]) -> set[str]:
        keywords: set[str] = set()
        for document in documents.values():
            keywords = keywords.union(set(document))
        return keywords

    @staticmethod
    def _invert(
        documents: dict[str, list[str]],
        keywords: set[str],
    ) -> dict[str, tuple[str]]:
        return {
            keyword: tuple(
                document_id
                for document_id, document_content in documents.items()
                if (keyword in document_content)
            )
            for keyword in keywords
        }


if __name__ == "__main__":
    raise NotImplementedError(
        "This module is not intended to be run directly\n"
        "If you wish to use it, import `InvertedIndex`\n"
        "If you wish to test it, run `test_inverted_index.py`"
    )
