import unittest

from main import extract_title

class TestExtrackTitle(unittest.TestCase):
  def test_one_line(self):
    markdown = "# Hello World"

    self.assertEqual(extract_title(markdown), "Hello World")

  def test_two_lines(self):
    markdown = "# Hello World\n## Subtitle"

    self.assertEqual(extract_title(markdown), "Hello World")

  def test_missing_title(self):
    markdown = "Hello World"

    with self.assertRaises(Exception):
      extract_title(markdown)

    markdown2 = "#Subtitle"

    with self.assertRaises(Exception):
      extract_title(markdown2)

  def test_with_more_whitespaces(self):
    markdown = "#  Hello World  "

    self.assertEqual(extract_title(markdown), "Hello World")

if __name__ == "__main__":
  unittest.main()
