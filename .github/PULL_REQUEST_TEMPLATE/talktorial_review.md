<!-- Talktorial review template -->
<!-- Thank you very much for helping us improve/extend TeachOpenCADD! -->

# Talktorial review

This PR template is suitable for adding new talktorials and extending existing talktorials (if you are doing the latter, answer bullet points w.r.t. your extensions).

## Details

* Talktorial ID: XXX
* Title: XXX
* Original authors: XXX
* Reviewer(s): XXX
* Date of review: DD-MM-YYYY

## Content

* One line summary: XXX
* Potential labels or categories (e.g. machine learning, small molecules, online APIs): XXX
* Time it took to execute (approx.):
* [ ] I have used the [talktorial template](https://github.com/volkamerlab/teachopencadd/blob/master/teachopencadd/talktorials/T000_template/talktorial.ipynb) and followed the content and formatting suggestions there
* [ ] _Packages_ must be open-sourced and should be installable from `conda-forge`. If you are adding new packages to the TeachOpenCADD environment, please check if already installed packages can perform the same functionality and if not leave a sentence explaining why the new addition is needed. If the new package is not on `conda-forge`, please list them and their intended usage here.
  * `package1`: Already in TeachOpenCADD
  * `package2` (conda-forge): I use it for XXX
  * `package3` (pip only): I use it for XXX
* [ ] _Data_ must be publicly available, preferably accessible via a webserver or downloadable via a URL. Please list the data resources that you use and how to access them:
  * Resource 1 (link to resource): Access via XXX
  * Resource 2 (link to resource): Access via XXX

## Content style

* [ ] Talktorial includes cross-references to other talktorials if applicable
* [ ] The table of contents reflects the talktorial story-line; order of #, ##, ### headers is correct
* [ ] URLs are linked with meaningful words, instead of pasting the URL directly or linking words like `here`.
* [ ] I have spell-checked the notebook
* [ ] Images have enough resolution to be rendered with quality, without being _too_ heavy.
* [ ] All figures have a description
* [ ] Markdown cell content is still in-line with code cell output (whenever results are discussed)
* [ ] I have checked that cell outputs are not incredibly long (this applies also to `DataFrames`)
* [ ] Formatting looks correctly on the Sphinx render (bold, italics, figure placing)

## Code style

* [ ] Variable and function names follow snake case rules (e.g. `a_variable_name` vs `aVariableName`)
* [ ] Spacing follows PEP8 (run Black on the code cells if needed)
* [ ] Code line are under 99 characters each (run `black-nb -l 99`)
* [ ] Comments are useful and well placed
* [ ] There are no unpythonic idioms like `for i in range(len(list))` (see slides)
* [ ] All 3rd party dependencies are listed at the top of the notebook
* [ ] I have marked all code cell with output referenced in markdown cells with the label `# NBVAL_CHECK_OUTPUT`
* [ ] I have identified potential candidates for a code refactor / useful functions
* [ ] All `import ...` lines are at the top (practice part) cell, ordered by standard library / 3rd party packages / our own (`teachopencadd.*`)
* [ ] I have used absolute paths instead of relative paths
  ```python
  HERE = Path(_dh[-1])
  DATA = HERE / "data"
  ```

## Website
We present our talktorials on our TeachOpenCADD website (https://projects.volkamerlab.org/teachopencadd/), so we have to check as well if the Jupyter notebook renders nicely there.

* [ ] If this PR adds a new talktorial, please follow these steps:
  * [ ] Add your talktorial to the complete list of talktorials [here](https://github.com/volkamerlab/teachopencadd/blob/master/docs/all_talktorials.rst) (at the end).
  * [ ] Add your talktorial to one or multiple of the collections [here](https://github.com/volkamerlab/teachopencadd/blob/master/docs/talktorials.rst). Or propose a new collection section in your PR.
  * [ ] Please complile the website following the instructions [here](https://github.com/volkamerlab/teachopencadd/tree/master/docs).
* [ ] Check the rendering of the talktorial of this PR.
* [ ] Is your talktorial listed [in the talktorial list](https://projects.volkamerlab.org/teachopencadd/all_talktorials.html)?
* [ ] Is your talktorial listed [in the talktorial collections](https://projects.volkamerlab.org/teachopencadd/talktorials.html)?
  * [ ] Add a picture for your talktorial in the collection view by following [these instructions](https://github.com/volkamerlab/teachopencadd/discussions/185). 
