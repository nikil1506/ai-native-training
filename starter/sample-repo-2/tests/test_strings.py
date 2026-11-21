import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from textkit.strings import slugify, truncate, word_count


class T(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_truncate(self):
        self.assertEqual(truncate("abcdefghij", 8), "abcde...")

    def test_word_count(self):
        self.assertEqual(word_count("a b c"), 3)


if __name__ == "__main__":
    unittest.main()
