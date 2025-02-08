# PyMind
This is a cross/platform static website generator that is designed to simple to use yet very extensible. All of the
markdown to HTML conversion is done by [Python Markdown](https://github.com/Python-Markdown/markdown), PyMind acts
basically as a wrapper around this project to feed the conversion tool as well as adding some bells and whistles.

# Quick Start
PyMind can be executed as a command line application, or be used as a Python module. But first you need to install it.
After cloning the repository, run `make install` in the PyMind directory.

> **Note**: The makefile is a bit rough, if you are getting an error try opening the makefile changing the `pipx` commands
> to `pip`.

Example of PyMind being used as an application
```bash
pymind -i [DIRECTORY TO SEARCH] -o [DIRECTORY TO OUTPUT HTML]
```

Example of PyMind being used as a module:
```python
import pymind

args = {"config": Path("path/to/pymind.toml")}

pymind.pymind(**args)
```

# Help
After installation, one can type `pymind -h` to output a help menu.

# Support
You may report bugs, ask for help, and discuss various other issues on the [bug
tracker](https://github.com/alexb7711/pymind/issues).
