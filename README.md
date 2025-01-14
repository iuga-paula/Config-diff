## Config diff
A python cmd tool that finds differences between 2 drupal config directories.
Useful when merging 2 repos into one.

## Usage
Run 
```shell
python3 findConfigDiff.py home/source_firectory home/destination_directory --removeUuids
```
## Results
The results can be found in .txt files created: ``results/different_content.txt`` and ``results/not_found_files.txt``
Missing files from source in destination can be found in: ``results/not_found_files.txt``
Files with the same name but different content can be found in: ``results/different_content.txt``


## Flags
Use the ``--removeUuids`` flag if you want to compare files removing uuid lines from configs.
Use the ``--showDiff`` flag if you want to receive different uuids form the different files in ``./patches``