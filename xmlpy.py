#!/usr/bin/env python3
import re

# HTML Parser credits to: https://limpet.net/mbrubeck/2014/08/11/toy-layout-engine-2.html

tag_name_regex = re.compile(r"[A-Za-z0-9\-_]")
config_factory_regex = re.compile(r"^ *### @xmlpy ([^\n]+)$", re.RegexFlag.MULTILINE)
html_elements = [ "<a>", "<abbr>", "<acronym>", "<address>", "<applet>", "<area>", "<article>", "<aside>", "<audio>", "<b>", "<base>", "<basefont>", "<bdi>", "<bdo>", "<big>", "<blockquote>", "<body>", "<br>", "<button>", "<canvas>", "<caption>", "<center>", "<cite>", "<code>", "<col>", "<colgroup>", "<data>", "<datalist>", "<dd>", "<del>", "<details>", "<dfn>", "<dialog>", "<dir>", "<div>", "<dl>", "<dt>", "<em>", "<embed>", "<fieldset>", "<figcaption>", "<figure>", "<font>", "<footer>", "<form>", "<frame>", "<frameset>", "<h1>", "<h2>", "<h3>", "<h4>", "<h5>", "<h6>", "<head>", "<header>", "<hr>", "<html>", "<i>", "<iframe>", "<img>", "<input>", "<ins>", "<kbd>", "<label>", "<legend>", "<li>", "<link>", "<main>", "<map>", "<mark>", "<meta>", "<meter>", "<nav>", "<noframes>", "<noscript>", "<object>", "<ol>", "<optgroup>", "<option>", "<output>", "<p>", "<param>", "<picture>", "<pre>", "<progress>", "<q>", "<rp>", "<rt>", "<ruby>", "<s>", "<samp>", "<script>", "<section>", "<select>", "<small>", "<source>", "<span>", "<strike>", "<strong>", "<style>", "<sub>", "<summary>", "<sup>", "<svg>", "<table>", "<tbody>", "<td>", "<template>", "<textarea>", "<tfoot>", "<th>", "<thead>", "<time>", "<title>", "<tr>", "<track>", "<tt>", "<u>", "<ul>", "<var>", "<video>", "<wbr>" ]

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

def get_first_element(string):
  parser = Parser(string)
  el = parser.parse_element()
  length = parser.index - 1

  return el, length

def transpile_element(element, xmlpy_factory):
  children = []

  for child in element.children:
    if type(child) == str:
      # child = re.sub(r"{{ *(.+?) *}}", lambda m: "{%s}" % m.group(1), child)
      child = re.sub(r"{ *(.+?) *}", lambda m: '\",%s,\"' % m.group(1), child)
      
      child = child.replace("'", "\\'")
      children.append('"' + child + '"')
    else: children.append(transpile_element(child, xmlpy_factory))
  
  attributes = []

  for attribute in element.attributes.keys():
    value = element.attributes[attribute]
    if value[1]:
      attributes.append("'%s': %s" % (attribute, value[0]))
    else:
      attributes.append("'%s': '%s'" % (attribute, value[0].replace("'", "\\'")))
  
  attrs = "{" + ', '.join(attributes) + "}"
  el_name = f"'{element.name}'" if "<" + element.name + ">" in html_elements else element.name
  return f"{xmlpy_factory}({el_name}, {attrs}, [{', '.join(children)}])"

def transpile_string(string, xmlpy_factory):
  code = ""
  
  is_str = False
  str_start = None
  
  ind = 0
  while ind < len(string):
    char = string[ind]

    if char in ['"', "'"] and not is_str:
      str_start = char
      is_str = True
    
    elif char == str_start and is_str and not (len(code) > 0 and code[-1] == "\\"):
      is_str = False

    elif char == "#":
      while string[ind] != "\n":
        ind += 1
      ind += 1
      continue

    elif char == "<" and not is_str:
      try:
        el, length = get_first_element(string[ind:])
        code += transpile_element(el, xmlpy_factory)
        ind += length + 1
        continue
      except Exception as e:
        if "Invalid tag name" not in str(e):
          raise e
    
    code += char
    ind += 1
  
  return code

if __name__ == "__main__":
  import sys
  import os
  from datetime import datetime

  rargs = sys.argv[1:]

  def printUsage():
    print("""Usage: python xmlpy.py <file>
  -o, --output <file>  : output file
  -f, --factory <name> : the element factory
  -h, --help           : show this help
  -n, --no-header      : don't write the xmlpy header""")

  if len(rargs) == 0:
    printUsage()
    exit(1)

  no_header = False
  output = None
  indx = 0
  xmlpy_factory = None

  args = []
  while indx < len(rargs):
    arg = rargs[indx]
    if arg.startswith("-"):
      if arg == "-h" or arg == "--help":
        printUsage()
        exit(0)
      elif arg == "-o" or arg == "--output":
        if indx + 1 >= len(rargs):
          printUsage()
          exit(1)
        indx += 1
        output = rargs[indx]
      elif arg == "-n" or arg == "--no-header":
        no_header = True
      elif arg == "-f" or arg == "--factory":
        if indx + 1 >= len(rargs):
          printUsage()
          exit(1)
        indx += 1
        xmlpy_factory = rargs[indx]
    else:
      args.append(arg)
    indx += 1

  if len(args) == 0:
    printUsage()
    print("Missing input file.")
    exit(1)

  cwd = os.getcwd()
  filep = os.path.join(cwd, args[0])
  if not os.path.exists(filep) or not os.path.isfile(filep):
    printUsage()
    print(f"'{filep}' is not a file.")
    exit(1)

  with open(filep, "r") as f:
    code = f.read()

  if not xmlpy_factory:
    mtch = re.search(config_factory_regex, code)
    if mtch:
      xmlpy_factory = mtch.group(1)
  
  outputfile = os.path.join(
    os.path.dirname(filep),
    os.path.splitext(os.path.basename(filep))[0] + ".py"
  )

  if output is not None:
    outputfile = os.path.join(cwd, output)

  content = ""
  if not no_header: content += f'# Source: {args[0]}, generated by xmlpy at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n'

  if not xmlpy_factory:
    xmlpy_factory = "PyElement"
    content += f"""class {xmlpy_factory}:
  def __init__(self, name, attributes, children):
    self.name = name
    self.attributes = attributes
    self.children = children

  def __repr__(self):
    return '<Element %s, %s, %s>' % (self.name, self.attributes, self.children)\n\n"""

  content += transpile_string(code, xmlpy_factory)

  with open(outputfile, "w") as f:
    f.write(content)