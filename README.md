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

### Costum elements
```py
class MyElement: pass

print(<MyElement something="test" />) # Element(MyElement, { something: 'test' }, [])
```

### Attribute templating
```py
print(<h1 style={{'color': 'red'}}>Hello, World!</h1>) # Element('h1', { style: { color: 'red' } }, [ 'Hello, World!' ])
```

### Body templating
```py
to = "World!"
print(<h1>Hello, { to }</h1>) # Element('h1', {}, [ "Hello, ", "World!" ])
```

### Element factories
By default XMLPy uses a class called `PyElement` to store html elements. To overwrite this include a comment like `### @xmlpy MyElement` or use `-f <name>` cli flag, where `MyElement` is a class that takes the name, attributes and children of the element.