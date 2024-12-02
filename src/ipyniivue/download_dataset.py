# Import necessary libraries
import os
import ipyniivue
import requests

def download_dataset(api_url, dest_folder):
    """Fetch and download files recursively."""
    print(f"Fetching contents from {api_url}...")
    os.makedirs(dest_folder, exist_ok=True)
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Failed to fetch {api_url}: {response.status_code}")
        return

    file_list = response.json()
    for item in file_list:
        item_type = item['type']
        download_url = item.get('download_url', '') if item_type == 'file' else ''
        name = item['name']
        path = item['path']

        if item_type == 'file':
            print(f"Downloading {name}...")
            file_response = requests.get(download_url)
            if file_response.status_code == 200:
                with open(os.path.join(dest_folder, name), 'wb') as f:
                    f.write(file_response.content)
            else:
                print(f"Failed to download {name}: {file_response.status_code}")
        elif item_type == 'dir':
            print(f"Entering directory {name}...")
            subfolder = os.path.join(dest_folder, name)
            sub_api_url = f"{api_url}/{name}"
            download_dataset(sub_api_url, subfolder)

    print(f"All files and subdirectories have been downloaded to {DEST_FOLDER}.")