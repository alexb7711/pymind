<!-- :nav: -->

# Configuring PyMind
PyMind is configured via a TOML file called `pymind.toml`. By default PyMind searches for the configuration search in
following directories for the configuration file:

- Linux/MacOS: `$HOME/.config/pymind`
- Windows: `$HOME\AppData\Local\Programs\pymind`.

## Configuration File Structure
Below is an example configuration file which is also used for the unit tests. Each table will be described in turn

``` toml
[IO]
input = "./tests/example" # In
output = "./tests/example-output"

[HTML]
css = "style.css"
footer = "footer.md"

[Markdown]
extensions = ["toc", "codehilite"]
```

## IO
This table contains the input and output directories to search for markdown files and to output HTML files, respectively.

- `input`: Relative or absolute path to the input directory
- `output`: Relative or absolute path to the output directory

## HTML
This table contains the names of the CSS file and footer markdown file that are desired to be used during the processing
of your static website. Note that these are just the file names. The files themselves are expected to be placed in the
default configuration directory.

> Maybe the path of the files can be based on the path of the configuration file?

- `css`: Name of the CSS file you wish to use
- `footer`: Name of the footer markdown file you wish to use

## Markdown
The markdown table allows the user to specify the [officially supported
extensions](https://python-markdown.github.io/extensions/). The specified extensions will be used to generate each
markdown file found in the `input` directory.

- `extensions`: A list of strings specifying Python markdown extensions.
