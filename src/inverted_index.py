import json
from os import walk

from utils import ParseUtils, ReadUtils


class InvertedIndex:
    def __init__(self, debug: bool = False):
        self.documents = ReadUtils.read_messages_element()
        searchable_documents: dict[str, list[str]] = {
            document_id: ParseUtils.parse(document_content)
            for document_id, document_content in self.documents.items()
        }
        self.keywords = self._extract(searchable_documents)
        self.index = self._invert(searchable_documents, self.keywords)
        if debug:
            with open("documents/index.json", mode="w", encoding="utf-8") as file:
                json.dump(self.index, file)

    def search(self, query: str) -> set[str]:
        terms: list[str] = ParseUtils.parse(query)
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
        "* If you wish to use it, import `InvertedIndex`\n"
        "* If you wish to test it, run `test_inverted_index.py`"
    )
