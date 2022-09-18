import argparse
import nbformat
import os


def process_file(filename, file_size_threshold, max_cell_output_size):
    # Bail out early if the file is not large enough
    if os.path.getsize(filename) <= file_size_threshold:
        return

    # Read the notebook
    with open(filename) as f:
        nb = nbformat.read(f, as_version=4)

    # Clear output of cells that are too large
    for cell in nb.cells:
        if sum(len(output.get("text", "")) for output in cell.outputs) > max_cell_output_size:
            cell.outputs = []

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
