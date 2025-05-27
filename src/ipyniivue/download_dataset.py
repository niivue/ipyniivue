"""
Downloads the data needed to run provided examples.

This module is designed to download the nii files needed to run examples and is
set to do so if another url is not provided. It can, however, download other
data, like fonts, from the NiiVue repo or elsewhere.
"""

# Import necessary libraries
import os
from pathlib import Path

import requests

import ipyniivue

# GitHub API URL for the base folder
BASE_API_URL = (
    "https://api.github.com/repos/niivue/niivue/contents/packages/niivue/demos/images"
)

DATA_FOLDER = Path(ipyniivue.__file__).parent / "images"


def download_dataset(api_url=None, dest_folder=None, force_download=False, files=None):
    """
    Download the datasets used for demos and testing.

    Parameters
    ----------
    api_url : str, optional
        The API URL to fetch the dataset from. Defaults to the base URL.
    dest_folder : Path, optional
        The destination folder to save the downloaded files. Defaults to the
        images directory in ipyniivue.
    force_download : bool, optional
        If True, download files even if they already exist locally. Defaults to
        False.
    files : list of str, optional
        A list of file paths (relative to the base API URL) to download. If
        None, all files will be downloaded.

    Raises
    ------
    FileNotFoundError
        If a specified file is not found in the dataset.
    Exception
        If a file cannot be downloaded due to HTTP errors.
    """
    if api_url is None:
        api_url = BASE_API_URL
    if dest_folder is None:
        dest_folder = DATA_FOLDER

    # Ensure the destination folder exists
    os.makedirs(dest_folder, exist_ok=True)

    # If files are specified, download only those files
    if files is not None:
        # For each file specified, attempt to download it
        for file_path in files:
            # Construct the full API URL for the file
            file_api_url = (
                "https://api.github.com/repos/niivue/niivue/contents/"
                f"packages/niivue/demos/images/{file_path}"
            )
            print(f"Fetching file info from {file_api_url}...")

            # Fetch file metadata from GitHub API
            response = requests.get(file_api_url)
            if response.status_code != 200:
                raise FileNotFoundError(
                    f"File {file_path} not found in the dataset. HTTP Status "
                    f"Code: {response.status_code}"
                )
            file_info = response.json()

            # Determine the output path
            local_file_path = dest_folder / file_path
            # Create subdirectories if needed
            local_file_path.parent.mkdir(parents=True, exist_ok=True)

            if local_file_path.exists() and not force_download:
                print(f"File {local_file_path} already exists. Skipping...")
                continue

            download_url = file_info.get("download_url")
            if not download_url:
                raise Exception(
                    f"No download URL found for {file_path}. Cannot proceed "
                    f"with download."
                )

            print(f"Downloading {file_path}...")
            file_response = requests.get(download_url)
            if file_response.status_code == 200:
                with local_file_path.open("wb") as f:
                    f.write(file_response.content)
            else:
                raise Exception(
                    f"Failed to download {file_path}: HTTP Status Code "
                    f"{file_response.status_code}"
                )

    else:
        # If no specific files are specified, download everything recursively
        print(f"Fetching contents from {api_url}...")
        response = requests.get(api_url)
        if response.status_code != 200:
            print(f"Failed to fetch {api_url}: HTTP Status Code {response.status_code}")
            return

        file_list = response.json()
        for item in file_list:
            item_type = item["type"]
            name = item["name"]
            path = item["path"]  # Relative path in the repository

            if item_type == "file":
                out_path = dest_folder / name
                if out_path.exists() and not force_download:
                    print(f"File {out_path} already exists. Skipping...")
                    continue
                download_url = item.get("download_url", "")
                print(f"Downloading {path}...")
                file_response = requests.get(download_url)
                if file_response.status_code == 200:
                    with out_path.open("wb") as f:
                        f.write(file_response.content)
                else:
                    print(
                        f"Failed to download {path}: HTTP Status Code "
                        f"{file_response.status_code}"
                    )
            elif item_type == "dir":
                subfolder = dest_folder / name
                sub_api_url = f"{api_url}/{name}"
                download_dataset(sub_api_url, subfolder, force_download)

    print(f"Dataset has been downloaded to {dest_folder}.")
