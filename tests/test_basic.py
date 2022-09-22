import filecmp
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

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
            raise RuntimeError
