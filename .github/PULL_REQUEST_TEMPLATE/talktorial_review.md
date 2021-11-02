<!-- Talktorial review template -->
<!-- Thank you very much for helping us improve TeachOpenCADD! -->

# Talktorial review

## Details

* Talktorial ID: ###
* Title: XXXXXXXXXXXXXXXXXXXXX
* Original authors: XXXXXXXXX
* Reviewer(s):
* Date of review:

## Content review

* Potential labels or categories (e.g. machine learning, small molecules, online APIs): XXXXXXXX
* One line summary: XXXXXXXXXX
* [ ] I have used the [talktorial template](https://github.com/volkamerlab/teachopencadd/blob/master/teachopencadd/talktorials/T000_template/talktorial.ipynb) and followed the formatting suggested there
* [ ] The table of contents reflects the talktorial story-line; order of #, ##, ### headers is correct
* [ ] URLs are linked with meaningful words, instead of pasting the URL directly or linking words like `here`.
* [ ] I have spell-checked the notebook
* [ ] Images have enough resolution to be rendered with quality, without being _too_ heavy.
* [ ] All figures have a description
* [ ] Markdown cell content is still in-line with code cell output (whenever results are discussed)
* [ ] I have checked that cell outputs are not incredibly long (this applies also to `DataFrames`)
* [ ] Formatting looks correctly on the Sphinx render (bold, italics, figure placing)

## Code review

* Time it took to execute (approx.):
* [ ] Variable and function names follow snake case rules (e.g. `a_variable_name` vs `aVariableName`)
* [ ] Spacing follows PEP8 (run Black on the code cells if needed)
* [ ] Code line are under 99 characters each (run `black -l 99`)
* [ ] Comments are useful and well placed
* [ ] There are no unpythonic idioms like `for i in range(len(list))` (see slides)
* [ ] All 3rd party dependencies are listed at the top of the notebook
* [ ] I have marked all code cell with output referenced in markdown cells with the label `# NBVAL_CHECK_OUTPUT`
* [ ] I have identified potential candidates for a code refactor / useful functions
* [ ] All `import ...` lines are at the top (practice part) cell, ordered by standard library / 3rd party packages / our own (`teachopencadd.*`)
* [ ] I have update the relative paths to absolute paths.
  ```python
  HERE = Path(_dh[-1])
  DATA = HERE / "data"
  ```
* List here unfamiliar libraries you find in the imports and their intended use: