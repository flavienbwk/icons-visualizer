import os
import shutil
import hashlib
from pathlib import Path

def create_directory(path):
    path = str(path)
    if os.path.exists(path) is False:
        try:
            os.makedirs(path)
        except OSError:
            print("Failed to create directory {}".format(path))
            return False
        else:
            print("Successfully created the directory {}".format(path))
    return True
    
def remove_directory(path):
    path = str(path)
    if os.path.exists(path) is True:
        try:
            shutil.rmtree(path)
        except Exception as e:
            print(e)
            print("Failed to remove directory {}".format(path))
            return False
        else:
            print("Successfully removed the directory {}".format(path))
    return True

def list_rglob_files(source_dir, patterns: list, exclude_dirs: list = []):
    all_files = []
    for pattern in patterns:
        files = []
        for filename in Path(source_dir).rglob(pattern):
            path_data = Path(filename)
            basename = path_data.name
            parent_directory = str(path_data.parent).replace(source_dir, "")
            parent_directories = str(parent_directory).strip("/").split("/")
            _, extension = os.path.splitext(basename)
            if parent_directory in exclude_dirs or parent_directories[0] in exclude_dirs:
                continue
            abs_path = str(path_data.absolute())
            files.append({
                "id": hashlib.md5(abs_path.encode()).hexdigest(),
                "parent": str(path_data.parent),
                "path": abs_path,
                "filename": basename,
                "extension": extension.lstrip(".")
            })
        all_files.extend(files)
    return all_files
