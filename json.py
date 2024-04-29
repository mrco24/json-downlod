import os
import json
import argparse
import requests
from urllib.parse import urlparse

def download_package_lock_json(url, folder_name):
    response = requests.get(url)
    if response.status_code == 200:
        package_lock_data = response.json()
        with open(os.path.join(folder_name, 'package-lock.json'), 'w') as f:
            json.dump(package_lock_data, f, indent=4)
    else:
        print("Failed to download package-lock.json from the URL:", url)

def main():
    parser = argparse.ArgumentParser(description="Download package-lock.json file from a list of URLs")
    parser.add_argument("-f", "--file", help="File containing URLs", required=True)
    args = parser.parse_args()

    file_path = args.file

    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return

    with open(file_path, 'r') as f:
        urls = f.readlines()

    for url in urls:
        url = url.strip()  # Remove trailing newline characters
        parsed_url = urlparse(url)
        # Extracting subdomain from URL
        subdomain = parsed_url.netloc
        folder_name = subdomain if subdomain else "unknown_subdomain"  # Use "unknown_subdomain" if subdomain not found
        os.makedirs(folder_name, exist_ok=True)
        download_package_lock_json(url, folder_name)

    print("package-lock.json files downloaded successfully!")

if __name__ == "__main__":
    main()
