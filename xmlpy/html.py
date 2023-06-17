import re

tag_name_regex = re.compile(r"[A-Za-z0-9\-_]")

# HTML Parser credits to: https://limpet.net/mbrubeck/2014/08/11/toy-layout-engine-2.html
class Element:
  def __init__(self, name, attributes, children):
    self.name = name
    self.attributes = attributes
    self.children = children
  
  def __repr__(self):
    return '<Element %s, %s, %s>' % (self.name, self.attributes, self.children)

class Parser:
  def __init__(self, string):
    self.string = string
    self.index = 0

  def next_char(self): return self.string[self.index] if self.index < len(self.string) else None
  def starts_with(self, ch): return self.string[self.index:].startswith(ch)
  def eof(self): return self.index >= len(self.string)

  def consume(self):
    cur = self.string[self.index]
    self.index += 1
    return cur
  
  def consume_while(self, predicate):
    result = ''
    while not self.eof() and predicate(self.next_char()):
      result += self.consume()
    return result
  
  def consume_whitespace(self):
    return self.consume_while(lambda ch: ch.isspace())
  
  def parse_tag_name(self):
    assert re.match(tag_name_regex, self.next_char()), "Invalid tag name"
    return self.consume_while(lambda ch: re.match(tag_name_regex, ch))
  
  def parse_node(self):
    if self.next_char() == "<":
      return self.parse_element()
    return self.parse_text()
  
  def parse_text(self):
    return self.consume_while(lambda ch: ch != "<")
  
  def parse_element(self):
    assert self.consume() == "<"
    tag_name = self.parse_tag_name()
    self.consume_whitespace()

    if self.next_char() == "/":
      self.consume()
      self.consume_whitespace()
      assert self.consume() == ">"
      return Element(tag_name, {}, [])
    
    attributes = self.parse_attributes()
    
    if self.next_char() == "/":
      self.consume()
      self.consume_whitespace()
      assert self.consume() == ">"
      return Element(tag_name, attributes, [])

    assert self.consume() == ">"

    children = self.parse_nodes()

    assert self.consume() == "<"
    assert self.consume() == "/"
    assert self.parse_tag_name() == tag_name
    assert self.consume() == ">"

    return Element(tag_name, attributes, children)
  
  def parse_attribute(self):
    name = self.parse_tag_name()
    
    if self.next_char() == "=":
      assert self.consume() == "="
      value = self.parse_attribute_value()
      return (name, value)
    else:
      return (name, (True, True))
  
  def parse_attribute_value(self):
    open_q = self.consume()

    if open_q == "{":
      
      value = ""
      bcount = 0
      while not self.eof():
        ch = self.consume()

        if ch == "{": bcount += 1
        if ch == "}":
          if bcount > 0: bcount -= 1
          else: break
        
        value += ch
      self.index -= 1

      assert self.consume() == "}"
      return value, True
    
    assert open_q == '"' or open_q == "'"
    value = self.consume_while(lambda ch: ch != open_q)
    assert self.consume() == open_q
    return value, False
  
  def parse_attributes(self):
    attributes = {}
    
    while True:
      self.consume_whitespace()
      if self.next_char() in ">/":
        break
      name, value = self.parse_attribute()
      attributes[name] = value
    
    return attributes
  
  def parse_nodes(self):
    nodes = []

    while True:
      self.consume_whitespace()
      if self.eof() or self.starts_with("</"):
        break
      nodes.append(self.parse_node())

    return nodes