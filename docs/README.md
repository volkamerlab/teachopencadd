# Compiling opencadd's Documentation

The docs for this project are built with [Sphinx](http://www.sphinx-doc.org/en/master/).
To compile the docs, first ensure that Sphinx and the ReadTheDocs theme are installed.


```bash
conda install sphinx sphinx_rtd_theme
```


Once installed, you can use the `Makefile` in this directory to compile static HTML pages by
```bash
make html
```

The compiled docs will be in the `_build` directory and can be viewed by opening `index.html` (which may itself
be inside a directory called `html/` depending on what version of Sphinx is installed).