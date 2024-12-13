## Config diff
A python cmd tool that finds differences between 2 drupal config directories.
Useful when merging 2 repos into one.

## Usage
Run 
```shell
python3 findConfigDiff.py home/source_firectory home/destination_directory
```
You see the results in txt files created: ``results/different_content.txt`` and ``results/not_found_files.txt``