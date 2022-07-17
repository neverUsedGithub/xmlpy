# XMLPy
XMLPy adds html and basic html templating to python.

# How to use?

1. `git clone https://github.com/neverUsedGithub/xmlpy/`
2. `cd xmlpy`
3. `python3 xmlpy.py`

# Examples
### Hello, World!
```jsx
print(<h1>Hello, World!</h1>)
```

### Attribute templating
```jsx
print(<h1 style={{'color': 'red'}}>Hello, World!</h1>)
```

### Body Templating
```jsx
to = "World!"
print(<h1>Hello, {{ to }}</h1>)
```

### Costum element class
XMLPy uses a class called `Element` to store html elements. If you want to use your own class you need to create something like:
```py
class Element:
  def __init__(self, name, attributes, children):
    # Do anything with name, attributes and children
```
