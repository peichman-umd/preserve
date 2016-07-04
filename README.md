## Command-Line Digital Preservation Utilities

This script includes the following subcommands:

  - bytecount (bc): Sum the bytes of (visible) files in the specified path, and also count them by extension.
  - inventory (inv): Create a CSV report containing file metadata for all visible files in the specified path. Write CSV to an output file (specified with -o flag) or send the data to stdout for further processing. Resume previously interrupted jobs by specifying path to an existing (with -e flag) partial inventory file.
  - compare (comp): Compare any number of file lists previously generated by various untilities, to ensure that the filesets are identical. Supported reports include those created by this script, tab-delimited File Analyzer reports, or Tivoli Storage Manager Backup reports.
  - verify (ver): Compare two existing inventory CSVs or inventories generated at runtime, by verifying their filenames and checksums (in the current implementation, filenames are assumed to be unique).
  
To install the script, clone this repository and do:

    python setup.py install

To run it, do:

    preserve bc [path]
    preserve inv [path] (-o OUTFILE) (-e EXISTING)
    preserve comp [file1] [file2] ...
    preserve ver [file1|path1] [file2|path2]
    preserve -h (for additional help)
