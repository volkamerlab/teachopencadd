# T017 · Advanced NGLview usage

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Jaime Rodríguez-Guerra, 2021, [Volkamer lab, Charité](https://volkamerlab.org/)
- Dominique Sydow, 2021, [Volkamer lab, Charité](https://volkamerlab.org/)


## Aim of this talktorial

[NGLView](http://nglviewer.org/nglview/latest/) is a powerful Jupyter widget that allows you to show molecular structures in your notebooks in a 3D interactive view! It supports both single conformations and trajectories, as well as a plethora of representations. In this talktorial we will cover how to use it in different scenarios, from simpler cases to more intricate ones.


### Contents in *Theory*

* NGL and NGLView
* NGL object model and terminology


### Contents in *Practical*

* First steps: make sure everything works!
    * Experiment with the interactive controls
* Basic API usage:
    * Show a structure using its PDB identifier
    * Show a structure using a local file
    * Saving the widget state as a screenshot for offline viewing
    * Customize the representations
    * Control representations by selections
    * NMR and multimodel structures
    * Load more than one structure
    * Show and hide components
* Advanced usage:
    * Custom coloring schemes and representations
    * Add geometric objects at selected atoms
    * Create interactive interfaces
    * Access the JavaScript layer
* Troubleshooting tips:
    * Check which Jupyter platform you are working from
    * How to install `nglview`, the right way


### References

* **NGL manuscript**: Rose *et al.*, <i>Nucl Acids Res.</i> (2015), <b>43</b> (W1), W576-W579 (https://academic.oup.com/nar/article/43/W1/W576/2467902)
* [NGL documentation](http://nglviewer.org/ngl/api/) and [repository](https://github.com/nglviewer/ngl)
* **NGLView manuscript**: Nguyen *et al.*, <i>Bioinformatics</i> (2018), <b>34</b> (7), 1241-1242 (https://academic.oup.com/bioinformatics/article/34/7/1241/4721781)
* [NGLView documentation](http://nglviewer.org/nglview/latest/) and [repository](https://github.com/nglviewer/nglview)
* [NGLView Q&A issues](https://github.com/nglviewer/nglview/issues?q=is%3Aissue+label%3AQ%26A). A lot of hidden knowledge in these conversations!
* [NGLView examples](https://github.com/nglviewer/nglview/tree/master/examples)
* [Jupyter Widgets (IPyWidgets)](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20Basics.html)
