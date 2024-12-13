import os
import hashlib
import sys

ignored_files = ['copernicus.settings', 'matomo.settings',
                 'system.site',
                 'views.view.content_listings',
                 'views.view.search',
                 'webform.webform.contact',
                 'block.block']


def calculate_hash(file_path):
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'r') as f:
            for line in f:
                # Skip uuids and config hashes
                if line.strip().startswith("uuid:") or line.strip().startswith("default_config_hash:"):
                    continue
                # Update the hash with the remaining content
                hasher.update(line.encode('utf-8'))
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def compareFiles(source_dir, destination_dir):
    notFoundTxt = open("../results/not_found_files.txt", "w")
    differentFilesTxt = open("../results/different_content.txt", "w")
    file_map = {}

    # Map source files
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.startswith(tuple(ignored_files)):
                continue
            file_path = os.path.join(root, file)
            file_map[file_path] = calculate_hash(file_path)

    # Check differences
    for file_path, file_hash in file_map.items():
        destination_file_path = file_path.replace(source_dir, destination_dir)
        configName = destination_file_path.replace(destination_dir, '')
        configName = configName.lstrip('/')
        if not os.path.isfile(destination_file_path):
            notFoundTxt.write(configName + "\n")
            print("Config not found in destination path: " + configName)
            continue
        if file_hash != calculate_hash(destination_file_path):
            differentFilesTxt.write(configName + "\n")
            print("Different config files for the same file: " + configName)

    notFoundTxt.close()
    differentFilesTxt.close()


def __main__():
    if len(sys.argv) - 1 < 2:
        print("Not enough arguments. Provide source and destination config dirs!")
        sys.exit(2)
    source = sys.argv[1]
    destination = sys.argv[2]
    if not os.path.isdir(source):
        print(f"Source {source} is not a directory!")
        sys.exit(2)
    if not os.path.isdir(destination):
        print(f"Destination {destination} is not a directory!")
        sys.exit(2)

    compareFiles(source, destination)


__main__()
