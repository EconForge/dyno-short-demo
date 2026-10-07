"""Execute and refresh the committed example notebooks in the Pixi environment.

The notebooks are the editable source of truth. Run with:
    pixi run python generate_notebooks.py
"""

from pathlib import Path
import json
import os
import sys
import tempfile

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parent
NOTEBOOKS = [
    "01_getting_started.ipynb",
    "02_deterministic_models.ipynb",
    "03_dynare_compatibility.ipynb",
    "04_reports_and_pipeline.ipynb",
]


def execute_notebook(path: Path) -> None:
    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=120,
        kernel_name="python3",
        resources={"metadata": {"path": str(ROOT)}},
        allow_errors=False,
    )
    executed = client.execute()
    for cell in executed.cells:
        cell.metadata.pop("execution", None)
    nbformat.write(executed, path)
    print(f"Executed {path.name}")


def main() -> None:
    # Use the active Pixi interpreter even if a user's global python3
    # kernelspec points at another checkout.
    with tempfile.TemporaryDirectory(prefix="dyno-notebook-kernel-") as temp_dir:
        kernel_dir = Path(temp_dir) / "kernels" / "python3"
        kernel_dir.mkdir(parents=True)
        (kernel_dir / "kernel.json").write_text(json.dumps({
            "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
            "display_name": "Python 3 (Pixi)",
            "language": "python",
        }), encoding="utf-8")
        previous_path = os.environ.get("JUPYTER_PATH")
        os.environ["JUPYTER_PATH"] = temp_dir + (os.pathsep + previous_path if previous_path else "")
        try:
            for name in NOTEBOOKS:
                execute_notebook(ROOT / name)
        finally:
            if previous_path is None:
                os.environ.pop("JUPYTER_PATH", None)
            else:
                os.environ["JUPYTER_PATH"] = previous_path


if __name__ == "__main__":
    main()
