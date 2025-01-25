![](https://github.com/OWNER/REPOSITORY/actions/workflows/WORKFLOW-FILE/badge.svg)

# PyMind
This project is another static website generator with the primary goal of being very simple, yet extremely extensible.
Pymind uses [Python Markdown](https://github.com/Python-Markdown/markdown), so you can use its features seamlessly (see
[configuring Pymind]()). To see what PyMind offers, see the [Features page]().

# Quick Start
PyMind can be executed as a command line application, or be used as a Python module. But first we need to install it.
After cloning the repository, run `make install` in the PyMind directory

**Note**: The makefile is a bit rough, if you are getting an error try opening the makefile changing the `pipx` commands
to `pip`.

Example of PyMind being used as an application
```bash
pymind -i [DIRECTORY TO SEARCH] -o [DIRECTORY TO OUTPUT HTML]
```

Example of PyMind being used as a module:
```python
import pymind

args = {"config": Path("path/to/pymind.toml")}

pymind.pymind(**args)

## Support
You may report bugs, ask for help, and discuss various other issues on the [bug
tracker](https://github.com/alexb7711/pymind/issues).
