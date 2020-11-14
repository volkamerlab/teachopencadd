"""
This script takes our talktorials and renders the first markdown cell
of the notebook to the corresponding README.md in the containing folder.
"""


def first_markdown_cells(path, stopif=lambda cell: "## Theory" in cell["source"]):
    import nbformat

    nb = nbformat.read(path, nbformat.NO_CONVERT)
    for cell in nb.cells:
        if stopif(cell):
            break
        if cell["cell_type"] == "markdown":
            yield cell["source"]


if __name__ == "__main__":
    import sys

    nbcontent = "\n".join(list(first_markdown_cells(sys.argv[1])))
    if not nbcontent.strip():  # empty results
        nbcontent = "> This talktorial is still under development"
    print(nbcontent)
