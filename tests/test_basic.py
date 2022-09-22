import filecmp
import shutil
import subprocess
import tempfile
from pathlib import Path

import nbformat

root = Path(__file__).parent.parent


def test_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        input_file = root / "tests" / "input.ipynb"
        expected_output_file = root / "tests" / "expected_output.ipynb"

        test_file = tmpdir / "output.ipynb"

        # Copy the input file to the output file
        shutil.copyfile(input_file, test_file)

        # Run `nb_clear_output.py` on the output file
        subprocess.check_call(["python", root / "nb_clear_output.py", test_file])

        if filecmp.cmp(test_file, expected_output_file):
            print("Test passed: no diffs found")
        else:
            print("Test failed: diffs found between", test_file, "and", expected_output_file)
            subprocess.run(["diff", test_file, expected_output_file])
            raise AssertionError

        # Check that cleared cells are cleared and non-cleared cells are not cleared
        with open(test_file) as f:
            nb = nbformat.read(f, as_version=4)

        for cell in nb.cells:
            if not cell.source:
                continue
            first_line = cell.source.splitlines()[0]
            if first_line == "# this cell output should be kept":
                assert cell.outputs
            elif first_line == "# this cell output should be cleared":
                assert not cell.outputs
            else:
                raise AssertionError(f"unexpected first line: {first_line!r}")
