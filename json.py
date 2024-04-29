import os
import json
import argparse
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

def download_package_lock_json(url_folder_tuple):
    url, folder_name, verbose = url_folder_tuple
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        package_lock_data = response.json()
        with open(os.path.join(folder_name, 'package-lock.json'), 'w') as f:
            json.dump(package_lock_data, f, indent=4)
        if verbose:
            print(f"Downloaded package-lock.json from {url} and saved in {folder_name} folder.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download package-lock.json from the URL: {url}")
        print(e)

def main():
    parser = argparse.ArgumentParser(description="Download package-lock.json file from a list of URLs")
    parser.add_argument("-f", "--file", help="File containing URLs", required=True)
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    parser.add_argument("-t", "--threads", type=int, help="Number of threads to use for downloading", default=1)
    args = parser.parse_args()

    file_path = args.file

    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return

    with open(file_path, 'r') as f:
        urls = f.readlines()

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for url in urls:
            url = url.strip()  # Remove trailing newline characters
            parsed_url = urlparse(url)
            # Extracting full subdomain from URL
            full_subdomain = parsed_url.netloc.replace('.', '_')
            folder_name = full_subdomain if full_subdomain else "unknown_domain"  # Use "unknown_domain" if subdomain not found
            os.makedirs(folder_name, exist_ok=True)
            executor.submit(download_package_lock_json, (url, folder_name, args.verbose))

    print("package-lock.json files downloaded successfully!")

if __name__ == "__main__":
    main()
