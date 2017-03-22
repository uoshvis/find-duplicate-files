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

import os
from sys import argv, exit
from hashlib import sha256              # collision-resistant and safer than md5

usage = 'Usage: >> python find_duplicate_files.py folder OR >> python find_duplicate_files.py folder1 folder2 folder3'

def hash_file(path, blocksize = 65536):
    '''
    Calculate the sha256 of a given file
    by reading binary data in blocks of 2**16
    The function receives the path to the file and
    returns the HEX digest of that file
    '''
    with open(path, 'rb') as afile:
        hasher = sha256()
        while True:
            buf = afile.read(blocksize)
            if not buf:
                break
            hasher.update(buf)
    return hasher.hexdigest()
    
def find_dup_size(folder):
    '''
    Finds duplicates by file size.
    Dups in format {filesize: [filepath]} 
    '''
    dups ={}
    for dirName, subdirs, fileList in os.walk(folder):
        print('Scanning %s ...'% dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Get sizes
            file_size = os.path.getsize(path)
            # Add or append the file path
            if file_size in dups:
                dups[file_size].append(path)
            else:
                dups[file_size] = [path]
    return dups
    
def find_dup_hash(file_list):
    '''
    Compares equal size files by hashfile
    '''
    print('Comparing: ')
    for filename in file_list:
        print('   {}'.format(filename))
    dups = {}
    for path in file_list:
        file_hash = hash_file(path)
        if file_hash in dups:
            dups[file_hash].append(path)
        else:
            dups[file_hash] = [path]
    return dups
    
def join_dicts(dict1, dict2):
    '''
    Joins two dictionaries
    '''
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]

def write_results(dict1, folders):
    '''
    Writes results to output file
    '''
    results = list(filter(lambda x: len(x)>1, dict1.values()))
    with open('duplicates.txt', 'w', encoding='utf-8') as f:
        f.write('Folders scanned: ' + str(folders)+ '\n')
        if len(results) > 0:
            f.write('Duplicates Found:\n')
            f.write('The following files are indentical. The name could differ, but the content is identical\n')
            f.write('----'*15 + '\n')
            for result in results:  
                for subresult in result:
                    f.write('\t\t%s\n' % subresult)
                f.write('----'*15 + '\n')
            print('Please, see the duplicates.txt file in your computer!')
        else:
            print('No duplicate file found')
            f.write('No duplicate file found')
        
def main(argv):
    '''
    Do the main work with directories given as argv
    '''    
    if len(argv) > 1:
        dup_size = {}
        folders = argv[1:]
        for folder in folders:                              # iterate the folders given
            if os.path.exists(folder):
                join_dicts(dup_size, find_dup_size(folder))    # find the duplicated files by size and append them to the dup_size
            else:
                print('%s is not a valid path, please verify' % folder)
                exit(1)                
        print('Comparing files with the same size... ')
        dups = {}
        for dup_list in dup_size.values():
            if len(dup_list) > 1:
                join_dicts(dups, find_dup_hash(dup_list))   # find duplicated by hash from dup_size
        write_results(dups, folders)
    else:
        print(usage)
        exit(2)

if __name__ == '__main__':
    main(argv)  