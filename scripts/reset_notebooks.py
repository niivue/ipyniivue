import json
import pathlib

EXAMPLE_FOLDER = pathlib.Path(__file__).parent.parent / "examples"

def reset_notebook(path):
    """
    Reset a Jupyter notebook to its initial state.

    Parameters:
    ----------
    path : str
        Absolute path to the notebook file from the notebooks directory.
    """
    with open(path) as f:
        notebook_data = json.load(f)

    for cell in notebook_data["cells"]:
        if cell["cell_type"] == "code":
            cell["outputs"] = []
            cell["execution_count"] = None

    if "metadata" in notebook_data:
        notebook_data["metadata"] = {"language_info": {"name": "python"}}

    with open(path, "w") as f:
        json.dump(notebook_data, f, indent=2)

for notebook_file in EXAMPLE_FOLDER.glob("*.ipynb"):
    print(f"Resetting {notebook_file}")
    reset_notebook(str(notebook_file))
