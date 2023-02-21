import os
import tarfile
import zipfile


def check_valid_path(path: str) -> str:
    """
    Check if the input path is a folder. If it is a compressed file, extract the
    folder inside and return its path.

    Args:
        path (str): A string representing the path to be checked.

    Returns:
        str: A string representing the path to the folder inside the compressed
        file or the original input path if it is a folder.

    Raises:
        ValueError: If the input path is None, or it is not a folder and it is not
        a supported compressed file type.
    """
    if not path:
        raise ValueError(
            f"Path cannot be None. Please enter a valid path: {path}")
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
        try:
            with extract_method(path, 'r') as ref:
                folder_name = os.path.splitext(os.path.basename(path))[0]
                extract_path = os.path.join(os.path.dirname(path), folder_name)
                ref.extractall(extract_path)
                return extract_path
        except (zipfile.BadZipfile, tarfile.ReadError) as e:
            raise ValueError(f"File could not be opened successfully:") from e

    # if the path is not a folder or a supported compressed file type, raise an exception
    raise ValueError(f"Please enter a valid path: {path}")


def list_files(input_dir):
    """
    Return a list of file paths in the specified directory.

    This function uses the `os.scandir` method to efficiently list files in the
    directory, which can handle large numbers of files more efficiently than
    using `os.listdir`. Each item in the returned list is the full path to a
    file in the directory.

    Args:
        input_dir (str): The path to the directory to list files from.

    Returns:
        A list of file paths in the specified directory.
    Raises:
        FileNotFoundError: If the specified directory does not exist or is not a directory.
        ValueError: If the specified directory does not contain any files.
    """
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"{input_dir} does not exist.")
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"{input_dir} is not a directory.")

    files = [os.path.join(input_dir, f.name) for f in os.scandir(input_dir) if f.is_file()]

    if not files:
        raise ValueError(f"{input_dir} does not contain any files.")

    return files
