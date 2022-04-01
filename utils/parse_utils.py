from nltk import word_tokenize
from nltk.corpus import stopwords


class ParseUtils:
    """
    Wrapper around a single method that is used to
    normalize a string into a searchable format.
    """

    @staticmethod
    def parse(string: str) -> list[str]:
        """
        Normalizes a string into a searchable format.
        :param string: Raw string
        :return: Tokenized lowercase string with no punctuation or stopwords
        """
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
