# find-duplicate-files
Finds duplicate files in given directories.
Starts by finding files with the same size and computes sha256 of those to find duplicates.
Thus we can find duplicates with different filename but same content
Returns duplicate files in duplicates.txt output file

Originally taken from:
http://pythoncentral.io/finding-duplicate-files-with-python/

Usage:
'>> python find_duplicate_files.py folder'
OR 
>> python find_duplicate_files.py folder1 folder2 folder3
