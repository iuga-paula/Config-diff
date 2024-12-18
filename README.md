## Config diff
A python cmd tool that finds differences between 2 drupal config directories.
Useful when merging 2 repos into one.

## Usage
Run 
```shell
python3 findConfigDiff.py home/source_firectory home/destination_directory --removeUUIDs
```
Use the ``--removeUUIDs`` flag if you want to compare files removing uuid lines from configs.
The results can be found in .txt files created: ``results/different_content.txt`` and ``results/not_found_files.txt``