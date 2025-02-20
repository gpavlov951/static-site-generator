import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
  def test_correct_prop_values(self):
    tag = "div"
    value = "This is a div"
    children = []
    props = {"class": "container"}
    node = HTMLNode(tag, value, children, props)
    self.assertEqual(node.tag, tag)
    self.assertEqual(node.value, value)
    self.assertEqual(node.children, children)
    self.assertEqual(node.props, props)

  def test_props_to_html(self):
    tag = "div"
    value = "This is a div"
    children = []
    props = {"class": "container", "id": "main"}
    node = HTMLNode(tag, value, children, props)
    self.assertEqual(node.props_to_html(), ' class="container" id="main"')

  def test_props_to_html_none(self):
    tag = "div"
    value = "This is a div"
    children = []
    props = None
    node = HTMLNode(tag, value, children, props)
    self.assertEqual(node.props_to_html(), "")

  def test_repr(self):
    tag = "div"
    value = "This is a div"
    children = []
    props = {"class": "container", "id": "main"}
    node = HTMLNode(tag, value, children, props)
    printed_value = node.__repr__()
    self.assertEqual(f"""HTMLNode
    Tag: {tag}
    Value: {value}
    Children: {children}
    Props:  class="container" id="main"
    """, printed_value)

class TestLeafNode(unittest.TestCase):
  def test_correct_prop_values(self):
    tag = "div"
    value = "This is a div"
    props = {"class": "container"}
    node = LeafNode(tag, value, props)
    self.assertEqual(node.tag, tag)
    self.assertEqual(node.value, value)
    self.assertEqual(node.props, props)

  def test_to_html(self):
    tag = "div"
    value = "This is a div"
    props = {"class": "container"}
    node = LeafNode(tag, value, props)
    self.assertEqual(node.to_html(), '<div class="container">This is a div</div>')

    p_node = LeafNode("p", "This is a paragraph of text.")
    self.assertEqual(p_node.to_html(), '<p>This is a paragraph of text.</p>') 

    a_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    self.assertEqual(a_node.to_html(), '<a href="https://www.google.com">Click me!</a>')

  def test_to_html_no_tag(self):
    value = "This is a div"
    props = {"class": "container"}
    node = LeafNode(None, value, props)
    self.assertEqual(node.to_html(), 'This is a div')

  def test_to_html_no_value(self):
    tag = "div"
    props = {"class": "container"}
    node = LeafNode(tag, None, props)
    with self.assertRaises(ValueError):
      node.to_html()

  def test_repr(self):
    tag = "div"
    value = "This is a div"
    props = {"class": "container"}
    node = LeafNode(tag, value, props)
    printed_value = node.__repr__()
    self.assertEqual(f"""LeafNode
    Tag: {tag}
    Value: {value}
    Props:  class="container"
    """, printed_value)

class TestParentNode(unittest.TestCase):
  def test_correct_prop_values(self):
    tag = "div"
    children = []
    props = {"class": "container"}
    node = ParentNode(tag, children, props)
    self.assertEqual(node.tag, tag)
    self.assertEqual(node.children, children)
    self.assertEqual(node.props, props)

  def test_to_html_no_tag(self):
    children = []
    props = {"class": "container"}
    node = ParentNode(None, children, props)
    with self.assertRaises(ValueError):
      node.to_html()

  def test_to_html_no_children(self):
    tag = "div"
    props = {"class": "container"}
    node = ParentNode(tag, None, props)
    with self.assertRaises(ValueError):
      node.to_html()

  def test_to_html(self):
    leaf1 = LeafNode("b", "Bold text") 
    leaf2 = LeafNode(None, "Normal text")
    leaf3 = LeafNode("i", "italic text")
    expected_html = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'

    node = ParentNode("p", [leaf1, leaf2, leaf3, leaf2])
    self.assertEqual(node.to_html(), expected_html)

  def test_to_html_nested_parents(self):
    leaf1 = LeafNode("b", "Bold text") 
    leaf2 = LeafNode(None, "Normal text")
    leaf3 = LeafNode("i", "italic text")
    expected_html = '<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>'

    node = ParentNode("div", [ParentNode("p", [leaf1, leaf2, leaf3, leaf2])])
    self.assertEqual(node.to_html(), expected_html)

    node2 = ParentNode("div", [ParentNode("p", [ParentNode("section", [ParentNode("p", [leaf1, leaf2])]), leaf2, leaf3, leaf2]), ParentNode("p", [leaf1, leaf2, leaf3, leaf2])])
    expected_html2 = '<div><p><section><p><b>Bold text</b>Normal text</p></section>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>'
    self.assertEqual(node2.to_html(), expected_html2)


if __name__ == "__main__":
  unittest.main()