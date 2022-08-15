import argparse
import os
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file-size-threshold", type=int, default=10 * 1024)
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    filenames = [filename for filename in args.files if os.path.getsize(filename) > args.file_size_threshold]
    try:
        subprocess.check_call([sys.executable, "-m", "jupyter", "nbconvert", "--clear-output", "--inplace", *filenames])
    except Exception:
        for filename in filenames:
            subprocess.check_call([sys.executable, "-m", "jupyter", "nbconvert", "--clear-output", "--inplace", filename])


if __name__ == "__main__":
    main()
