class HTMLNode():
  def __init__(self, tag: str=None, value: str=None, children: object=None, props: dict=None) -> None:
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError()

  def props_to_html(self):
    if self.props == None:
      return ""

    mapped_items = map(lambda item: f' {item[0]}="{item[1]}"', self.props.items())
    return "".join(mapped_items)
  
  def __repr__(self) -> str:
    return f"""HTMLNode
    Tag: {self.tag}
    Value: {self.value}
    Children: {self.children}
    Props: {self.props_to_html()}
    """

class ParentNode(HTMLNode):
  def __init__(self, tag: str, children: list, props: dict=None) -> None:
    super().__init__(tag, None, children, props)

  def to_html(self):
    if self.tag == None:
      raise ValueError("Tag is required for ParentNode")

    if self.children == None:
      raise ValueError("Children is required for ParentNode")

    children_html = "".join(map(lambda child: child.to_html(), self.children))

    return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

  def __repr__(self) -> str:
    return f"""ParentNode
    Tag: {self.tag}
    Children: {self.children}
    Props: {self.props_to_html()}
    """

class LeafNode(HTMLNode):
  def __init__(self, tag: str, value: str, props: dict=None) -> None:
    super().__init__(tag, value, None, props)

  def to_html(self):
    if self.value == None:
      raise ValueError("Value is required for LeafNode")

    if self.tag == None:
      return self.value

    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

  def __repr__(self) -> str:
    return f"""LeafNode
    Tag: {self.tag}
    Value: {self.value}
    Props: {self.props_to_html()}
    """