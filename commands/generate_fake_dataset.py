from setuptools import Command


class GenerateFakeDataset(Command):
    """
    A custom command for setuptools that generates a fake dataset of files containing random words.
    """
    description = 'Generate a fake dataset'
    user_options = [
        ('num-files=', None, 'The number of files to generate.'),
        ('min-words-per-file=', None, 'The minimum number of words per file.'),
        ('max-words-per-file=', None, 'The maximum number of words per file.'),
        ('output-dir=', None, 'The directory to write the generated files to.')
    ]

    def initialize_options(self):
        self.num_files = None
        self.min_words_per_file = None
        self.max_words_per_file = None
        self.output_dir = None

    def finalize_options(self):
        if self.num_files is None:
            raise ValueError("The 'num-files' option must be specified.")
        if self.min_words_per_file is None:
            raise ValueError("The 'min-words-per-file' option must be specified.")
        if self.max_words_per_file is None:
            raise ValueError("The 'max-words-per-file' option must be specified.")
        if self.output_dir is None:
            raise ValueError("The 'output-dir' option must be specified.")
        self.num_files = int(self.num_files)
        self.min_words_per_file = int(self.min_words_per_file)
        self.max_words_per_file = int(self.max_words_per_file)

    def run(self):
        from scripts.dataset import generate_fake_dataset
        generate_fake_dataset(
            num_files=self.num_files,
            min_words_per_file=self.min_words_per_file,
            max_words_per_file=self.max_words_per_file,
            output_dir=self.output_dir
        )
