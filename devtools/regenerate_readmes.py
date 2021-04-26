r"""
This script takes our talktorials and renders the first markdown cell
of the notebook to the corresponding README.md in the containing folder.

Usage
-----

.. code-block::

    % python devtools/regenerate_readmes.py --output README.md \
        teachopencadd/talktorials/T001_query_chembl/talktorial.ipynb

"""


def first_markdown_cells(path, stopif=lambda cell: "## Theory" in cell["source"]):
    import nbformat

    nb = nbformat.read(path, nbformat.NO_CONVERT)
    for cell in nb.cells:
        if stopif(cell):
            break
        if cell["cell_type"] == "markdown":
            yield cell["source"]


def parse_cli():
    from argparse import ArgumentParser

    p = ArgumentParser()
    p.add_argument("notebook", type=str)
    p.add_argument("--output", type=str, default=None)
    return p.parse_args()


def main():
    from pathlib import Path

    args = parse_cli()

    nbcontent = "\n\n\n".join(list(first_markdown_cells(args.notebook)))
    if not nbcontent.strip():  # empty results
        nbcontent = "> This talktorial is still under development"

    if args.output:
        with open(Path(args.notebook).parent / args.output, "w") as f:
            f.write(nbcontent + "\n")
    else:
        print(nbcontent)


if __name__ == "__main__":
    main()
