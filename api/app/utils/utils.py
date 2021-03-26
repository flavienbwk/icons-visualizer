import os
import hashlib
from pathlib import Path


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
                "parent": path_data.parent,
                "path": abs_path,
                "filename": basename,
                "extension": extension.lstrip(".")
            })
        all_files.extend(files)
    return all_files
