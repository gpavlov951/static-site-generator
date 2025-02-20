import unittest

from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, split_nodes_delimiter

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node, node2)

  def test_not_eq(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.CODE)
    self.assertNotEqual(node, node2)

  def test_default_url(self):
    node = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node.url, None)

  def test_correct_prop_values(self):
    text = "This is a text node"
    text_type = TextType.TEXT
    node = TextNode(text, text_type)
    self.assertEqual(node.text, text)
    self.assertEqual(node.text_type, text_type)

  def test_repr(self):
    text = "This is a text node"
    text_type = TextType.TEXT
    node = TextNode(text, text_type)
    printed_value = node.__repr__()
    self.assertEqual(f"TextNode({text}, {text_type}, None)", printed_value)

class TestTextNodeToHTMLNode(unittest.TestCase):
  def test_bold_text_type(self):
    text = "Bold text"
    text_type = TextType.BOLD
    text_node = TextNode(text, text_type)
    html_node = text_node_to_html_node(text_node)

    expected_html = "<b>Bold text</b>"
    self.assertEqual(html_node.to_html(), expected_html)

class TestTextToTextNodes(unittest.TestCase):
  def test_normal_text(self):
    text = "Hello world"
    nodes = text_to_textnodes(text)
    expected_nodes = [TextNode(text, TextType.TEXT)]

    self.assertEqual(nodes, expected_nodes)
  
  def test_bold_text(self):
    text = "Hello **world**"
    nodes = text_to_textnodes(text)
    expected_nodes = [
      TextNode("Hello ", TextType.TEXT),
      TextNode("world", TextType.BOLD)
    ]

    self.assertEqual(nodes, expected_nodes)

  def test_italic_text(self):
    text = "Hello _world_"
    nodes = text_to_textnodes(text)
    expected_nodes = [
      TextNode("Hello ", TextType.TEXT),
      TextNode("world", TextType.ITALIC)
    ]

    self.assertEqual(nodes, expected_nodes)
  
  def test_code_text(self):
    text = "Hello `world`"
    nodes = text_to_textnodes(text)
    expected_nodes = [
      TextNode("Hello ", TextType.TEXT),
      TextNode("world", TextType.CODE)
    ]

    self.assertEqual(nodes, expected_nodes)
  
  def test_link_text(self):
    text = "Hello [world](https://world.com)"
    nodes = text_to_textnodes(text)
    expected_nodes = [
      TextNode("Hello ", TextType.TEXT),
      TextNode("world", TextType.LINKS, "https://world.com")
    ]

    self.assertEqual(nodes, expected_nodes)

  def test_image_text(self):
    text = "Hello ![world](https://world.com)"
    nodes = text_to_textnodes(text)
    expected_nodes = [
      TextNode("Hello ", TextType.TEXT),
      TextNode("world", TextType.IMAGES, "https://world.com")
    ]

    self.assertEqual(nodes, expected_nodes)

  def test_multiple_text_types(self):
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    nodes = text_to_textnodes(text)
    expected_nodes = [
      TextNode("This is ", TextType.TEXT),
      TextNode("text", TextType.BOLD),
      TextNode(" with an ", TextType.TEXT),
      TextNode("italic", TextType.ITALIC),
      TextNode(" word and a ", TextType.TEXT),
      TextNode("code block", TextType.CODE),
      TextNode(" and an ", TextType.TEXT),
      TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
      TextNode(" and a ", TextType.TEXT),
      TextNode("link", TextType.LINKS, "https://boot.dev")
    ]

    self.assertEqual(nodes, expected_nodes)

class TestExtractMarkdownImages(unittest.TestCase):
  def test_one_image(self):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
    images = extract_markdown_images(text)
    expected_images = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]

    self.assertEqual(images, expected_images)

  def test_two_images(self):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and another ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
    images = extract_markdown_images(text)
    expected_images = [
      ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
      ("rick roll", "https://i.imgur.com/aKaOqIh.gif")
    ]

    self.assertEqual(images, expected_images)


class TestExtractMarkdownLinks(unittest.TestCase):
  def test_one_link(self):
    text = "This is text with a [rick roll](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
    links = extract_markdown_links(text)
    expected_links = [("rick roll", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")]

    self.assertEqual(links, expected_links)

  def test_two_links(self):
    text = "This is text with a [rick roll](https://www.youtube.com/watch?v=dQw4w9WgXcQ) and another [rick roll](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
    links = extract_markdown_links(text)
    expected_links = [
      ("rick roll", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
      ("rick roll", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    ]

    self.assertEqual(links, expected_links)

class TestSplitNodesImage(unittest.TestCase):
  def test_no_images(self):
    node = TextNode(
      "This is text with no images",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    expected_nodes = [node]

    self.assertEqual(new_nodes, expected_nodes)

  def test_no_matches(self):
    node = TextNode(
      "This is text with an image ![rick roll https://i.imgur.com/aKaOqIh.gif)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    expected_nodes = [node]

    self.assertEqual(new_nodes, expected_nodes)

  def test_one_image(self):
    node = TextNode(
      "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    expected_nodes = [
      TextNode("This is text with an image ", TextType.TEXT),
      TextNode("rick roll", TextType.IMAGES, "https://i.imgur.com/aKaOqIh.gif"),
    ]

    self.assertEqual(new_nodes, expected_nodes)

  def test_two_images(self):
    node = TextNode(
      "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and another ![rick roll](https://i.imgur.com/aKaOqIh.gif)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    expected_nodes = [
      TextNode("This is text with an image ", TextType.TEXT),
      TextNode("rick roll", TextType.IMAGES, "https://i.imgur.com/aKaOqIh.gif"),
      TextNode(" and another ", TextType.TEXT),
      TextNode("rick roll", TextType.IMAGES, "https://i.imgur.com/aKaOqIh.gif"),
    ]

    self.assertEqual(new_nodes, expected_nodes)
  
  def test_images_with_text_and_links(self):
    node = TextNode(
      "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to youtube](https://www.youtube.com/@bootdotdev)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    expected_nodes = [
      TextNode("This is text with an image ", TextType.TEXT),
      TextNode("rick roll", TextType.IMAGES, "https://i.imgur.com/aKaOqIh.gif"),
      TextNode(" and a link [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
    ]

    self.assertEqual(new_nodes, expected_nodes)


class TestSplitNodesLink(unittest.TestCase):
  def test_no_links(self):
    node = TextNode(
      "This is text with no links",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    expected_nodes = [node]

    self.assertEqual(new_nodes, expected_nodes)

  def test_no_matches(self):
    node = TextNode(
      "This is text with a link [to boot dev https://www.boot.dev) and [to youtube https://www.youtube.com/@bootdotdev)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    expected_nodes = [node]

    self.assertEqual(new_nodes, expected_nodes)

  def test_one_link(self):
    node = TextNode(
      "This is text with a link [to boot dev](https://www.boot.dev)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    expected_nodes = [
      TextNode("This is text with a link ", TextType.TEXT),
      TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
    ]

    self.assertEqual(new_nodes, expected_nodes)

  def test_two_links(self):
    node = TextNode(
      "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    expected_nodes = [
      TextNode("This is text with a link ", TextType.TEXT),
      TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
      TextNode(" and ", TextType.TEXT),
      TextNode("to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"),
    ]

    self.assertEqual(new_nodes, expected_nodes)

class TestSplitNodesDelimiter(unittest.TestCase):
  def test_two_bold_delimiters(self):
    node = TextNode("Hello **world** and **people**", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    expected_nodes = [
      TextNode("Hello ", TextType.TEXT),
      TextNode("world", TextType.BOLD),
      TextNode(" and ", TextType.TEXT),
      TextNode("people", TextType.BOLD)
    ]

    self.assertEqual(new_nodes, expected_nodes)

  def test_two_diff_delimiters(self):
    node = TextNode("Here is `code` and **bold** text", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    expected_nodes = [
      TextNode("Here is ", TextType.TEXT),
      TextNode("code", TextType.CODE),
      TextNode(" and ", TextType.TEXT),
      TextNode("bold", TextType.BOLD),
      TextNode(" text", TextType.TEXT)
    ]

    self.assertEqual(new_nodes, expected_nodes)

  def test_no_delimiters(self):
    node = TextNode("Just normal text", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    expected_nodes = [node]

    self.assertEqual(new_nodes, expected_nodes)

  def test_start_with_delimiter(self):
    node = TextNode("**Bold** text", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    expected_nodes = [
      TextNode("Bold", TextType.BOLD),
      TextNode(" text", TextType.TEXT)
    ]

    self.assertEqual(new_nodes, expected_nodes)

if __name__ == "__main__":
  unittest.main()