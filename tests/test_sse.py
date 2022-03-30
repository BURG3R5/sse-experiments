import unittest

from src.sse import SSE


class TestSSE(unittest.TestCase):
    sse: SSE

    @classmethod
    def setUpClass(cls):
        cls.sse = SSE(debug=True)

    def test_sse(self):
        # TODO
        pass


if __name__ == "__main__":
    unittest.main()
