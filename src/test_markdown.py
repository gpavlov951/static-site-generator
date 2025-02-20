import unittest

from markdown import markdown_to_blocks, markdown_to_html_node, BlockType, block_to_block_type

class TestMarkdownToBlock(unittest.TestCase):
  def test_single_block(self):
    text = "Hello world"
    blocks = markdown_to_blocks(text)
    expected_blocks = ["Hello world"]

    self.assertEqual(blocks, expected_blocks)

  def test_multiple_blocks(self):
    text = "Hello world\n\nThis is a new block"
    blocks = markdown_to_blocks(text)
    expected_blocks = ["Hello world", "This is a new block"]

    self.assertEqual(blocks, expected_blocks)
  
  def test_three_block(self):
    text = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

    blocks = markdown_to_blocks(text)
    expected_blocks = [
      "# This is a heading",
      "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
      "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
    ]

    self.assertEqual(blocks, expected_blocks)

  def test_with_empty_blocks(self):
    text = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.


* This is the first list item in a list block
* This is a list item
* This is another list item


"""

    blocks = markdown_to_blocks(text)
    expected_blocks = [
      "# This is a heading",
      "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
      "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
    ]

    self.assertEqual(blocks, expected_blocks)

class TestMarkdownToHtmlNode(unittest.TestCase):
  def test_single_paragraph(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
    )

  def test_multi_block(self):
    md = """# Main Title

This is a paragraph with some _italic_ and **bold** text.

## Second Level Heading

* First item
* Second item
* Third item with **bold** text

1. Ordered first
2. Ordered second
3. Ordered third
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><h1>Main Title</h1><p>This is a paragraph with some <i>italic</i> and <b>bold</b> text.</p><h2>Second Level Heading</h2><ul><li>First item</li><li>Second item</li><li>Third item with <b>bold</b> text</li></ul><ol><li>Ordered first</li><li>Ordered second</li><li>Ordered third</li></ol></div>",
    )

  def test_code_block(self):
    md = """```
def hello():
  print("Hello World")
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>def hello():\n  print(\"Hello World\")\n</code></pre></div>",
    )

  def test_quote_block(self):
    md = """> This is a quote block
> with multiple lines
> and some **bold** text
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><blockquote>This is a quote block with multiple lines and some <b>bold</b> text</blockquote></div>",
    )

class TestBlockToBlockType(unittest.TestCase):
  def test_heading_block(self):
    block = "# This is a heading"
    block_type = block_to_block_type(block)

    self.assertEqual(block_type, BlockType.HEADING)

    block2 = "## This is a heading"
    block_type2 = block_to_block_type(block2)

    self.assertEqual(block_type2, BlockType.HEADING)

  def test_code_block(self):
    block = "```\nThis is a code block\n```"
    block_type = block_to_block_type(block)

    self.assertEqual(block_type, BlockType.CODE)

    block2 = "```python\nThis is a code block\n```"
    block_type2 = block_to_block_type(block2)

    self.assertEqual(block_type2, BlockType.CODE)

  def test_quote_block(self):
    block = "> This is a quote"
    block_type = block_to_block_type(block)

    self.assertEqual(block_type, BlockType.QUOTE)

    block2 = "> This is a quote\n> This is another quote"
    block_type2 = block_to_block_type(block2)

    self.assertEqual(block_type2, BlockType.QUOTE)

  def test_unordered_list_block(self):
    block = "* This is a list item"
    block_type = block_to_block_type(block)

    self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    block2 = "- This is a list item"
    block_type2 = block_to_block_type(block2)

    self.assertEqual(block_type2, BlockType.UNORDERED_LIST)

  def test_ordered_list_block(self):
    block = "1. This is a list item"
    block_type = block_to_block_type(block)

    self.assertEqual(block_type, BlockType.ORDERED_LIST)

    block2 = "1. This is a list item"
    block_type2 = block_to_block_type(block2)

    self.assertEqual(block_type2, BlockType.ORDERED_LIST)

    block3 = "1. This is a list item\n2. This is another list item"
    block_type3 = block_to_block_type(block3)

    self.assertEqual(block_type3, BlockType.ORDERED_LIST)

  def test_paragraph_block(self):
    block = "This is a paragraph"
    block_type = block_to_block_type(block)

    self.assertEqual(block_type, BlockType.PARAGRAPH)

    block2 = "This is a paragraph\nThis is another paragraph"
    block_type2 = block_to_block_type(block2)

    self.assertEqual(block_type2, BlockType.PARAGRAPH)

    block3 = "Is not # heading"
    block_type3 = block_to_block_type(block3)

    self.assertEqual(block_type3, BlockType.PARAGRAPH)

__name__ == "__main__" and unittest.main()
