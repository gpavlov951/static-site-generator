import re
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
  TEXT = "normal"
  BOLD = "bold"
  ITALIC = "italic"
  CODE = "code"
  LINKS = "links"
  IMAGES = "images"

class TextNode():
  def __init__(self, text: str, text_type: TextType, url: str=None):
    self.text = text
    self.text_type = text_type
    self.url = url

  def __repr__(self) -> str:
    return f"TextNode({self.text}, {self.text_type}, {self.url})"

  def __eq__(self, value: object) -> bool:
    return self.text == value.text and self.text_type == value.text_type and self.url == value.url

def text_node_to_html_node(text_node):
  match text_node.text_type:
    case TextType.BOLD:
      return LeafNode("b", text_node.text)
    case TextType.ITALIC:
      return LeafNode("i", text_node.text)
    case TextType.CODE:
      return LeafNode("code", text_node.text) 
    case TextType.LINKS:
      return LeafNode("a", text_node.text, { "href": text_node.url })
    case TextType.IMAGES:
      return LeafNode("img", "", { "src": text_node.url, "alt": text_node.text })
    case TextType.TEXT:
      return LeafNode(None, text_node.text)
    case _:
      raise ValueError("Invalid TextType")

def text_to_textnodes(text):
  nodes = [TextNode(text, TextType.TEXT)]
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
  nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
  nodes = split_nodes_image(nodes)
  nodes = split_nodes_link(nodes)

  return nodes

def extract_markdown_images(text):
  return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
  return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
  nodes = []

  for node in old_nodes:
    # Skip non-text nodes
    if node.text_type != TextType.TEXT:
      nodes.append(node)
      continue

    current_text = node.text
    matches = extract_markdown_images(current_text)
    if len(matches) == 0:
      nodes.append(node)
      continue

    for match in extract_markdown_images(current_text):
      alt_text, url = match
      sections = current_text.split(f"![{alt_text}]({url})", 1)
      nodes.append(TextNode(sections[0], TextType.TEXT))
      nodes.append(TextNode(alt_text, TextType.IMAGES, url))
      current_text = sections[1]

    if current_text:
      nodes.append(TextNode(current_text, TextType.TEXT))

  return nodes

def split_nodes_link(old_nodes):
  nodes = []

  for node in old_nodes:
    # Skip non-text nodes
    if node.text_type != TextType.TEXT:
      nodes.append(node)
      continue

    current_text = node.text
    matches = extract_markdown_links(current_text)
    if len(matches) == 0:
      nodes.append(node)
      continue

    for match in matches:
      link_text, url = match
      sections = current_text.split(f"[{link_text}]({url})", 1)
      nodes.append(TextNode(sections[0], TextType.TEXT))
      nodes.append(TextNode(link_text, TextType.LINKS, url))
      current_text = sections[1]

    if current_text:
      nodes.append(TextNode(current_text, TextType.TEXT))

  return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for old_node in old_nodes:
      if old_node.text_type != TextType.TEXT:
          new_nodes.append(old_node)
          continue
      split_nodes = []
      sections = old_node.text.split(delimiter)
      if len(sections) % 2 == 0:
          raise ValueError("invalid markdown, formatted section not closed")
      for i in range(len(sections)):
          if sections[i] == "":
              continue
          if i % 2 == 0:
              split_nodes.append(TextNode(sections[i], TextType.TEXT))
          else:
              split_nodes.append(TextNode(sections[i], text_type))
      new_nodes.extend(split_nodes)
  return new_nodes
