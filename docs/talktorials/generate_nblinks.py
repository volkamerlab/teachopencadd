from pathlib import Path
import json

IGNORE = [
    "T000_template",
]


def create_nblink(notebook_path):
    d = {}
    d["path"] = str(notebook_path)
    d["extra-media"] = [str(notebook_path.parent / "images/")]
    return d


def main():
    talktorials = Path("../../teachopencadd/talktorials/")
    print(talktorials)
    for path in talktorials.glob("*/"):
        nbpath = path / "talktorial.ipynb"
        if not nbpath.exists():
            continue
        for ignore in IGNORE:
            if ignore in str(nbpath):
                break
        else:
            nblink = create_nblink(nbpath)
            with open(f"{path.stem}.nblink", "w") as f:
                print("Creating path for", nbpath)
                json.dump(nblink, f)


if __name__ == "__main__":
    main()
