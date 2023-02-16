import os
import tarfile
import zipfile


def check_valid_path(path: str) -> str:
    """Return if the input path is a folder, if it is a compressed file,
        extract the folder inside and return its path"""
    if os.path.isdir(path):
        return path

    extract_methods = {
        '.zip': zipfile.ZipFile,
        '.tar': tarfile.open,
        '.tgz': tarfile.open,
        '.tar.gz': tarfile.open,
    }

    filename, ext = os.path.splitext(path)
    ext = os.path.splitext(filename)[1] + ext
    if ext in extract_methods:
        extract_method = extract_methods[ext]
        with extract_method(path, 'r') as ref:
            folder_name = os.path.splitext(os.path.basename(path))[0]
            extract_path = os.path.join(os.path.dirname(path), folder_name)
            ref.extractall(extract_path)
            return extract_path

    # if the path is not a folder or a supported compressed file type, raise an exception
    raise ValueError(f"Unsupported file type: {path}")
