# XMLPy
XMLPy adds html and basic html templating to python.

# How to use?

1. `git clone https://github.com/neverUsedGithub/xmlpy/`
2. `cd xmlpy`
3. `python3 xmlpy.py`

# Examples
### Hello, World!
```py
print(<h1>Hello, World!</h1>) # Element('h1', {}, [ "Hello, World!" ])
```

### Costum Elements
```py
class MyElement: pass

print(<MyElement something="test" />) # Element(MyElement, { something: 'test' }, [])
```

### Attribute templating
```py
print(<h1 style={{'color': 'red'}}>Hello, World!</h1>) # Element('h1', { style: { color: 'red' } }, [ 'Hello, World!' ])
```

### Body Templating
```py
to = "World!"
print(<h1>Hello, { to }</h1>) # Element('h1', {}, [ "Hello, World!" ])
```

### Costum element class
XMLPy uses a class called `XMLPyElement` to store html elements. XMLPyElement take the name, attribute and children in the constructor. Example class: 
```py
class XMLPyElement:
  def __init__(self, name, attributes, children):
    # Do anything with name, attributes and children
```
