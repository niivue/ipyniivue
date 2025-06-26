"""
Downloads the data needed to run provided examples.

This module is designed to download the nii files needed to run examples and is
set to do so if another url is not provided. It can, however, download other
data, like fonts, from the NiiVue repo or elsewhere.
"""

from pathlib import Path

import requests

import ipyniivue

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

    dest_folder.mkdir(parents=True, exist_ok=True)

    if files:
        for file_path in files:
            local_file_path = dest_folder / file_path
            if local_file_path.exists() and not force_download:
                print(f"{file_path} already exists.")
                continue

            file_api_url = f"{api_url}/{file_path}"
            response = requests.get(file_api_url)
            if response.status_code != 200:
                raise FileNotFoundError(
                    f"File {file_path} not found (HTTP {response.status_code})."
                )

            content_type = response.headers.get("Content-Type")

            if (
                content_type
                and "application/json" in content_type.lower()
                and not file_path.endswith(".json")
            ):
                file_info = response.json()
                download_url = file_info.get("download_url")
                if not download_url:
                    raise Exception(f"No download URL for {file_path}.")
            else:
                download_url = file_api_url

            print(f"Downloading {file_path}...")
            file_response = requests.get(download_url)
            file_response.raise_for_status()
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            local_file_path.write_bytes(file_response.content)

    else:
        response = requests.get(api_url)
        response.raise_for_status()
        file_list = response.json()

        for item in file_list:
            if item["type"] != "file":
                continue

            local_file_path = dest_folder / item["name"]
            if local_file_path.exists() and not force_download:
                print(f"{item['name']} already exists.")
                continue

            print(f"Downloading {item['name']}...")
            download_url = item["download_url"]
            file_response = requests.get(download_url)
            file_response.raise_for_status()
            local_file_path.write_bytes(file_response.content)

    print(f"Dataset downloaded successfully to {dest_folder}.")
