import filecmp
import os
import shutil
import subprocess

# Define the input and output files for the test
input_file = "test_input.ipynb"
output_file = "test_output.ipynb"
expected_output_file = "expected_test_output.ipynb"

# Copy the input file to the output file
shutil.copyfile(input_file, output_file)

# Run `nb_clear_output.py` on the output file
subprocess.run(["python", "nb_clear_output.py", output_file])

# Check if the expected output file exists
if not os.path.exists(expected_output_file):
    # The expected output file does not exist yet, so use the current output file as the expected output
    shutil.copyfile(output_file, expected_output_file)
    print("Created new expected output file:", expected_output_file)
else:
    if filecmp.cmp(output_file, expected_output_file):
        print("Test passed: no diffs found")
    else:
        print("Test failed: diffs found between", output_file, "and", expected_output_file)
        subprocess.run(["diff", output_file, expected_output_file])
