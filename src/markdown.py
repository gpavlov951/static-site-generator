from enum import Enum
from htmlnode import ParentNode
from textnode import text_to_textnodes, text_node_to_html_node

def markdown_to_blocks(text):
  blocks = text.split("\n\n")
  return list(filter(lambda x: x != "", map(lambda x: x.strip(), blocks)))

def markdown_to_html_node(markdown):
  # Split the markdown into blocks
  blocks = markdown_to_blocks(markdown)
  children = []

  for block in blocks:
    # determine the type of block
    html_node = block_to_html_node(block)
    children.append(html_node)
  return ParentNode("div", children, None)

def block_to_html_node(block):
  block_type = block_to_block_type(block)
  if block_type == BlockType.PARAGRAPH:
    return paragraph_to_html_node(block)
  if block_type == BlockType.HEADING:
    return heading_to_html_node(block)
  if block_type == BlockType.CODE:
    return code_to_html_node(block)
  if block_type == BlockType.QUOTE:
    return quote_to_html_node(block)
  if block_type == BlockType.UNORDERED_LIST:
    return unordered_list_to_html_node(block)
  if block_type == BlockType.ORDERED_LIST:
    return ordered_list_to_html_node(block)

  raise ValueError(f"Unknown block type: {block_type}")

def text_to_children(text):
  text_nodes = text_to_textnodes(text)
  children = []

  for text_node in text_nodes:
    html_node = text_node_to_html_node(text_node)
    children.append(html_node)

  return children

def paragraph_to_html_node(block):
  lines = block.split("\n")
  paragraph = " ".join(lines)
  children = text_to_children(paragraph)
  return ParentNode("p", children) 

def heading_to_html_node(block):
  level = 0

  for char in block:
    if char != "#":
      break
    level += 1
  
  if level + 1 >= len(block) or block[level] != " ":
    raise ValueError(f"Invalid heading level: {level}")

  text = block[level + 1:]
  children = text_to_children(text)
  return ParentNode(f"h{level}", children)

def code_to_html_node(block):
  if not block.startswith("```") or not block.endswith("```"):
    raise ValueError("Invalid code block")
  text = block[4:-3]
  children = text_to_children(text)
  code = ParentNode("code", children)
  return ParentNode("pre", [code])

def quote_to_html_node(block):
  lines = block.split("\n")
  new_lines = []
  for line in lines:
    if not line.startswith(">"):
      raise ValueError("Invalid quote block")
    new_lines.append(line.lstrip(">").strip())
  content = " ".join(new_lines)
  children = text_to_children(content)
  return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
  lines = block.split("\n")
  items = []
  for line in lines:
    if not line.startswith("* ") and not line.startswith("- "):
      raise ValueError("Invalid unordered list block")
    text = line[2:]
    children = text_to_children(text)
    items.append(ParentNode("li", children))
  return ParentNode("ul", items)

def ordered_list_to_html_node(block):
  lines = block.split("\n")
  items = []
  for i, line in enumerate(lines):
    if not line.startswith(f"{i+1}. "):
      raise ValueError("Invalid ordered list block")
    text = line[3:]
    children = text_to_children(text)
    items.append(ParentNode("li", children))
  return ParentNode("ol", items)

class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
  is_heading = block.startswith("#")
  if is_heading:
    return BlockType.HEADING

  is_code = block.startswith("```") and block.endswith("```")
  if is_code:
    return BlockType.CODE

  is_quote = block.startswith(">")
  if is_quote:
    return BlockType.QUOTE

  is_unordered_list = all([line.startswith("* ") or line.startswith("- ") for line in block.split("\n")])
  if is_unordered_list:
    return BlockType.UNORDERED_LIST

  is_ordered_list = all([line.startswith(f"{i+1}. ") for i, line in enumerate(block.split("\n"))])
  if is_ordered_list:
    return BlockType.ORDERED_LIST

  return BlockType.PARAGRAPH

