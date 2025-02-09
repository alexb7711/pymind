# Footer
The footer plugin allows the user to inject a custom footer into each page being converted by PyMind. The file with the
footer text should be saved in the [configuration file directory](configuration) directory. The name of the file is
specified in the configuration file under the `HTML` table:

```toml
[HTML]
footer = "footer.md"
```

The footer plugin will read in the markdown file, convert it to HTML, and then inject the footer HTML within a footer
tag.
