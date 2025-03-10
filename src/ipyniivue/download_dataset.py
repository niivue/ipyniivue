"""
Downloads the data needed to run provided examples.

This module is designed to download the nii files needed to run examples
and is set to do so if another url is not provided. It can, however, download
other data, like fonts, from the NiiVue repo or elsewhere.
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


def download_dataset(api_url=None, dest_folder=None, force_download=False):
    """
    Download the datasets used for demos and testing.

    Parameters
    ----------
    api_url
        Option to provide a custom url to download data.
    dest_folder
        Option to provide a custom folder to store the data.
    force_download
        If true, download datasets even if they are already available locally.
    """
    if api_url is None:
        api_url = BASE_API_URL
    if dest_folder is None:
        dest_folder = DATA_FOLDER

    # Fetch and download files recursively.
    print(f"Fetching contents from {api_url}...")
    os.makedirs(dest_folder, exist_ok=True)
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Failed to fetch {api_url}: {response.status_code}")
        return

    file_list = response.json()
    for item in file_list:
        item_type = item["type"]
        download_url = item.get("download_url", "") if item_type == "file" else ""
        name = item["name"]

        if item_type == "file":
            out_path = dest_folder / name
            if out_path.exists() and not force_download:
                continue
            print(f"Downloading {name}...")
            file_response = requests.get(download_url)
            if file_response.status_code == 200:
                with out_path.open("wb") as f:
                    f.write(file_response.content)
            else:
                print(f"Failed to download {name}: {file_response.status_code}")
        elif item_type == "dir":
            print(f"Entering directory {name}...")
            subfolder = dest_folder / name
            sub_api_url = f"{api_url}/{name}"
            download_dataset(sub_api_url, subfolder)

    print(f"All files and subdirectories have been downloaded to {dest_folder}.")
