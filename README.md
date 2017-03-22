# find-duplicate-files
'''
Finds duplicate files in given directories.
Starts by finding files with the same size and computes sha256 of those to find duplicates.
Thus we can find duplicates with different filename but same content
Returns duplicate files in duplicates.txt output file

Originally taken from:
http://pythoncentral.io/finding-duplicate-files-with-python/

Modifications by:
https://github.com/IanLee1521/utilities/commit/263a0e63503d41df961a352772763e83cf69baf9#diff-880bd89719233299f79774650259c095L11
http://codereview.stackexchange.com/questions/93546/find-and-remove-duplicate-files-in-one-or-more-directories
'''

Single folder usage:
>> python find_duplicate_files.py folder

Multiple folders usage:
>> python find_duplicate_files.py folder1 folder2 folder3
