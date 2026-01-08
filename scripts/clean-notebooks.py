import os
import subprocess
import argparse

def clean_notebooks(root_dir):
    """
    Recursively traverse the directory tree starting at root_dir,
    and clean all Jupyter notebook files using nb-clean.

    Args:
        root_dir (str): The root directory to start searching for notebook files.
    """
    print(f"Starting to clean notebooks in directory: {root_dir}")
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.ipynb'):
                full_path = os.path.join(dirpath, filename)
                print(f"Cleaning notebook: {full_path}")
                subprocess.run([
                    'nb-clean', 'clean', full_path, '--remove-empty-cells', '--remove-all-notebook-metadata'
                ], check=True)

def main():
    parser = argparse.ArgumentParser(
        description='Recursively clean all Jupyter notebook files in a directory.'
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='The root directory to search (default: current directory).'
    )
    args = parser.parse_args()
    clean_notebooks(args.directory)

if __name__ == '__main__':
    main()