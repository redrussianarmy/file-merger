# File Merger

## How does it work?
A command-line tool was developed for merging multiple sorted text files into a single, sorted output file. The tool supports three different strategies for merging files, depending on the size of the input files and the desired performance characteristics:

**Basic strategy**: This strategy reads input files and lazily merge the input files, one element at a time and writes them to the output file. It is suitable for small inputs and performs all operations sequentially.

**Async strategy**: This strategy splits the input files into chunks and processes each chunk in a separate coroutine using asyncio. This allows for concurrent execution of the file processing, but does not use multiple threads. The sorted results from each chunk are then written to intermediate files that are merged at the end. This approach can be more efficient than the basic strategy for larger inputs, and can help reduce memory usage compared to the parallel strategy.

**Parallel strategy**: The parallel strategy uses multiprocessing to process each input file in a separate process. In this strategy, each input file is divided into chunks, and each chunk is processed by a separate subprocess in parallel. The results of the subprocesses are then combined at the end to create the final output file. The parallel strategy is suitable for very large inputs where the basic and async strategies may not be efficient due to the limitations of single-threaded or single-process approaches. By using parallel processing, this strategy can distribute the workload across multiple CPU cores, which can greatly improve the overall performance. The parallel strategy provides the best performance for very large inputs, while the async strategy offers a good compromise between performance and memory usage.

### Merge Algorithm

`heapq.merge` is a Python function that takes multiple sorted input iterables and merges them into a single sorted iterable. It works by creating a heap of the first item from each iterable, and repeatedly popping the smallest item from the heap and adding it to the output. When an iterable is exhausted, its next item is automatically pulled from the next iterable in the list. This process continues until all input iterables have been exhausted and the entire output is produced. The algorithm used by heapq.merge is a variation of the merge step in merge sort. It has a time complexity of O(n log k), where n is the total number of items in all input iterables and k is the number of input iterables. It does not hold all items in memory at once. It uses a heap data structure to merge the items from the input iterables one at a time, only keeping a small number of items in memory at any given time. This means that heapq.merge() is memory-efficient and can handle very large iterables without running out of memory. However, heapq.merge is a blocking operation that is run synchronously and cannot be run asynchronously.

         Input Iterable 1               Input Iterable 2           Input Iterable 3
          ┌───────────┐                 ┌─────────┐                ┌───────────┐
          │     A     │                 │   C     │                │     F     │
          ├───────────┤                 ├─────────┤                ├───────────┤
          │     B     │                 │   D     │                │     H     │
          ├───────────┤                 ├─────────┤                ├───────────┤
          │     E     │                 │   G     │                │     J     │
          └───────────┘                 └─────────┘                └───────────┘

                                       heapq.merge()
                                            │
                                            ▼
                                   ┌─────────────────┐
                                   │ Output Iterable │
                                   └─────────────────┘
                                            │
                                            ▼
          Output Iterable:    A     B     C     D     E     F     G     H     J

In general, the solution should be efficient and scalable for most use cases. The basic strategy is suitable for small inputs, while the async and parallel strategies provide improved performance for larger inputs. The parallel strategy provides the best performance, but requires more memory and may not be suitable for extremely large inputs. The async strategy provides a good compromise between performance and memory usage, and should be suitable for most inputs. However, the performance of each strategy will depend on the specifics of the input data, so it is always a good idea to test different strategies with different inputs to find the best approach for a given situation.

### Performance Comparison

| Input File Size | Number of Files | Basic         | Async  | Parallel |
| --------------- | --------------- | ------------- | ------ | -------- |
| 16 KB           | 5               | 0.01s         | 0.01s  | 0.35s    |
| 1.27 MB         | 500             | 0.4s          | 0.25s  | 0.59s    |
| 11.4 MB         | 4000            | 1.89s         | 1.25s  | 0.81s    |
| 39 MB           | 10000           | 10.51s        | 4.67s  | 3.12s    |
| 195 MB          | 50000           | 73.96s        | 33.70s | 13.43s   |
| 1 GB            | 250000          | 514.64s       | 150.29s| 79.70s   |

*Default parameters are used in performance measurements. File and Line chunk sizes are 1024, number of processes is 4.*

---
## Instructions

A directory containing hundreds of files is given. Each file contains a sorted list of hundreds of words, one word per line.

A python command line tool that aims to find an efficient and scalable solution that combines the contents of all files into a single sorted file.
An example output:

```
filemerger -i input_files_dir
```

1. word1
2. word2
......
10. word10

---

## Package Installation (optional)

If desired, the application can be installed with the following command:

```bash
python setup.py install
```
or

```bash
pip install .
```

*Note: Package installation is recommended. But it is not necessary to run the application*.

---

## Creating a Fake Dataset (optional)
You can create fake dataset for testing or development. The `faker` library is needed for this. If you have installed the `filemerger` package, it will come with faker.

Otherwise you need to run following command first.
```
pip install faker==17.0.0
```

Example fake dataset creation code is as follows.

```
python setup.py generate_fake_dataset --num-files 10 --min-words-per-file 100 --max-words-per-file 500 --output-dir dataset/small_dataset
```


---
## Usage

### With Installation

Once `filemerger` is installed, it can be run in one of two ways.

```filemerger --help```

### Without Installation

`filemerger` can also be run without installation. The method below can be followed:

Either modify permissions to make it executable and use a version of python3 to run it:

```bash
chmod +x file_merger.py
./file_merger.py --help
```

Or, the python command directly can run the tool.

```bash
python file_merger.py
```
---

## `filemerger` CLI

Command line tool has a help feature that shows all the operations that can be done.

```
$ filemerger --help
usage: file_merger.py [-h] [-i INPUT_DIR] [-o OUTPUT_DIR] [-f FILENAME] [-p] [-np N_OF_PROCESS] [-cf CHUNK_FILE] [-cl CHUNK_LINE]

A tool that merges all input files into a single sorted output file

options:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input-dir INPUT_DIR
                        A directory of files to be merged.
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        A directory where the merged file will be saved. DEFAULT <current-directory>
  -f FILENAME, --filename FILENAME
                        A name of output file. DEFAULT output.txt
  -p, --parallel        Use multiprocessing for merging operations. DEFAULT False
  -np N_OF_PROCESS, --n_of_process N_OF_PROCESS
                        Number of processes to use. DEFAULT 4
  -cf CHUNK_FILE, --chunk-file CHUNK_FILE
                        Number of files to process at once. DEFAULT 1024
  -cl CHUNK_LINE, --chunk-line CHUNK_LINE
                        Number of lines to process at once. DEFAULT 1024
```

---

## Examples

### Merge Multiple Files in Input Folder
Consider the input files in the following structure.
```
input_dir/
    ├── file1.dat
    ├── file2.dat
    ├── file3.dat
    ├── file4.dat
    └── file5.dat
```
The folder directory where the files are located is given as Input Directory.
```
$ filemerger -i input_dir

Operation is successful. The output file has been saved here: /path/to/package/folder/output.txt
```
---
### Merge Multiple Files in Compressed File
Compressed file directory can be given as Input Directory. In this case, the files in the compressed file are extracted to the folder created in the same directory and the directory of that folder is given.
```
$ filemerger -i compressed_file_dir

Operation is successful. The output file has been saved here: /path/to/package/folder/output.txt
```

---
### Custom Output Path
Specify a custom directory.
```
$ filemerger -i input_dir -o output_dir

Operation is successful. The output file has been saved here: /path/to/custom/folder/output.txt
```
---
### Custom Output File Name

```
$ filemerger -i input_dir -o output_dir -f merged_file.txt

Operation is successful. The output file has been saved here: /path/to/custom/folder/merged_file.txt
```
---
### Use Multiprocessing
Use multiple processes during the merge process
```
$ filemerger -i input_dir -p

Operation is successful. The output file has been saved here: /path/to/package/folder/output.txt
```
---
### Use Multiprocessing with Custom Number of Processes
Use custom number of processes
```
$ filemerger -i input_dir -p -np 8

Operation is successful. The output file has been saved here: /path/to/package/folder/output.txt
```
---
### Custom File Chunk Size
Set custom number of files to process at once
```
$ filemerger -i input_dir -cf 100

Operation is successful. The output file has been saved here: /path/to/package/folder/output.txt
```
---
### Custom Line Chunk Size
Set custom number of lines to process at once
```
$ filemerger -i input_dir -cl 250

Operation is successful. The output file has been saved here: /path/to/package/folder/output.txt
```
---
### Attempting to Enter an Invalid Input Directory
If the user enters an invalid input directory, the following error will be raised.

```
$ filemerger -i invalid_dir
Traceback (most recent call last):
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\Scripts\filemerger-script.py", line 33, in <module>
    sys.exit(load_entry_point('filemerger==1.0.0', 'console_scripts', 'filemerger')())
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\site-packages\merge_files\main.py", line 64, in cli_main
    merge(
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\site-packages\merge_files\main.py", line 12, in merge
    input_dir = check_valid_path(input_dir)
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\site-packages\merge_files\utils.py", line 36, in check_valid_path
    raise ValueError(f"Please enter a valid path: {path}")
ValueError: Please enter a valid path: invalid_dir
```
---
### Attempting to Not Enter a Input Directory
If the user doesn't enter any input directory, the following error will be raised.
```
$ filemerger
Traceback (most recent call last):
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\Scripts\filemerger-script.py", line 33, in <module>
    sys.exit(load_entry_point('filemerger==1.0.0', 'console_scripts', 'filemerger')())
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\site-packages\merge_files\main.py", line 64, in cli_main
    merge(
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\site-packages\merge_files\main.py", line 12, in merge
    input_dir = check_valid_path(input_dir)
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\site-packages\merge_files\utils.py", line 10, in check_valid_path
    raise ValueError(
ValueError: Path cannot be None. Please enter a valid path: None
```
---

## Tests

The core functions of `filemerger` have tests.

```
$ python setup.py test
running test
running egg_info
writing filemerger.egg-info\PKG-INFO
writing dependency_links to filemerger.egg-info\dependency_links.txt
writing entry points to filemerger.egg-info\entry_points.txt
writing top-level names to filemerger.egg-info\top_level.txt
reading manifest file 'filemerger.egg-info\SOURCES.txt'
writing manifest file 'filemerger.egg-info\SOURCES.txt'
running build_ext
(running tests...)

----------------------------------------------------------------------
Ran 30 tests in 0.143s

OK
```

---

## Coverage Report

You can see how much of the written unit tests cover the project code.

If you have installed the `filemerger` package, it will come with coverage package.

Otherwise you need to run following command first.
```
pip install coverage==7.1.0
```

Run following command to generage coverage report.
```
python setup.py coverage
```

Current coverage rate is 92%

| Module                          | statements | missing | excluded | coverage |
|---------------------------------|------------|---------|----------|----------|
| merge_files\__init__.py         |          1 |       0 |        0 |     100% |
| merge_files\__main__.py         |          3 |       3 |        0 |       0% |
| merge_files\main.py             |         34 |      10 |        0 |      71% |
| merge_files\mergers\async_.py   |         20 |       0 |        0 |     100% |
| merge_files\mergers\base.py     |         50 |       0 |        0 |     100% |
| merge_files\mergers\basic.py    |          4 |       0 |        0 |     100% |
| merge_files\mergers\parallel.py |         31 |       0 |        0 |     100% |
| merge_files\utils.py            |         31 |       0 |        0 |     100% |
| **Total**                       |    **174** |  **13** |    **0** |  **93%** |

---

## Improvements for the Future

1. **Compression:** The ability to compress input files and decompress the merged output file can greatly reduce storage and transfer costs for large files.
2. **User-friendly CLI:** The current command-line interface (CLI) is suitable for experienced users, but it can be improved for ease of use by novice users. Adding more descriptive error messages, help texts, and examples could make the tool more accessible to a wider range of users.
3. **Progress monitoring:** Providing a progress bar or other status updates during processing can help users to better understand the progress of the tool and make it more user-friendly.
4. **Integration with other tools:** Integrating the tool with other tools, such as a file transfer or backup tool, can provide a more complete solution for users.
5. **Performance profiling and optimization:** Conducting performance profiling and optimization on the codebase can help identify and fix bottlenecks, and further improve the performance of the tool.