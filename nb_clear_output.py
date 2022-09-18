import argparse
import nbformat
import os


def process_cell(cell, max_cell_output_size):
    # See: https://github.com/jupyter/nbconvert/blob/68b496b7fcf4cfbffe9e1656ac52400a24cacc45/nbconvert/preprocessors/clearoutput.py#L11
    
    # Calculate the total size of outputs
    output_size = 0
    for output in cell.outputs:
        output_size += len(output.get("text", ""))
        # Check the size of the `data` field for all MIME types
        if 'data' in output:
            output_size += sum(len(data) for _mime_type, data in output['data'].items())

    if output_size <= max_cell_output_size:
        # Output size is under the limit, we're OK.
        return
        
    cell.outputs = []
    cell.execution_count = None
    # Remove metadata associated with output
    if "metadata" in cell:
        for field in {'collapsed', 'scrolled'}:
            cell.metadata.pop(field, None)


def process_file(filename, file_size_threshold, max_cell_output_size):
    # Bail out early if the file is not large enough
    if os.path.getsize(filename) <= file_size_threshold:
        return

    # Read the notebook
    with open(filename) as f:
        nb = nbformat.read(f, as_version=4)

    # Clear output of cells that are too large
    for cell in nb.cells:
        process_cell(cell, max_cell_output_size)

    # Write the notebook
    with open(filename, "w") as f:
        nbformat.write(nb, f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file-size-threshold", type=int, default=10 * 1024)
    parser.add_argument("--max-cell-output-size", type=int, default=1024)
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    for filename in args.files:
        process_file(filename, args.file_size_threshold, args.max_cell_output_size)


if __name__ == "__main__":
    main()
