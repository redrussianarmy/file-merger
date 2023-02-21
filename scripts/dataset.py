from faker import Faker
import os
import random


def generate_fake_dataset(num_files: int, min_words_per_file: int,
                          max_words_per_file: int, output_dir: str) -> None:
    """
    Generates a fake dataset of files containing random words.

    Args:
        num_files (int): The number of files to generate.
        min_words_per_file (int): The minimum number of words per file.
        max_words_per_file (int): The maximum number of words per file.
        output_dir (str): The directory to write the generated files to.

    Raises:
        TypeError: If any of the arguments are not of the correct type.
        ValueError: If the value of min_words_per_file is greater than max_words_per_file.

    Returns:
        None.

    The function generates a fake dataset with a specified number of files and a random number of words per file.
    The words are generated using the Faker library and are sorted alphabetically before being written to the output files.

    If the output directory does not exist, it will be created. The files will be named 'file_0.dat', 'file_1.dat', etc.,
    and will be written to the specified output directory.

    Example:
        >>> generate_fake_dataset(num_files=10, min_words_per_file=100, max_words_per_file=500, output_dir='dataset/small_dataset')
    """
    if not isinstance(num_files, int) or not isinstance(min_words_per_file, int) or not isinstance(max_words_per_file, int):
        raise TypeError(
            "The arguments 'num_files', 'min_words_per_file', and 'max_words_per_file' must be integers.")

    if not isinstance(output_dir, str):
        raise TypeError("The argument 'output_dir' must be a string.")

    if min_words_per_file > max_words_per_file:
        raise ValueError(
            "The value of 'min_words_per_file' cannot be greater than 'max_words_per_file'.")

    # Set up the Faker generator
    fake = Faker()

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate and sort the words for each file
    for i in range(num_files):
        # Generate a random number of words for the file
        words_per_file = random.randint(min_words_per_file, max_words_per_file)
        # Generate the unique words
        words = set()
        while len(words) < words_per_file:
            words.add(fake.word().lower())
        # Sort the words
        words = sorted(words)
        # Write the words to the output file
        output_file = os.path.join(output_dir, f'file_{i}.dat')
        with open(output_file, 'w') as f:
            f.write('\n'.join(words))
    print("Fake dataset has been generated.")


if __name__ == "__main__":
    generate_fake_dataset(num_files=10, min_words_per_file=100,
                          max_words_per_file=500, output_dir='dataset/small_dataset')
