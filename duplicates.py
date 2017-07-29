import os
import sys
import hashlib
from collections import defaultdict
from argparse import ArgumentParser


def get_filepaths_in_folder(folder_path):
    filepaths = []
    for root, _, filenames in os.walk(folder_path):
        local_filepaths = [os.path.join(root, filename) for filename in filenames]
        filepaths += local_filepaths
    return filepaths


def compute_file_hash(byte_file):
    buffer_size = 65536  # 64kb
    md5 = hashlib.md5()
    received_data = byte_file.read(buffer_size)
    while received_data:
        md5.update(received_data)
        received_data = byte_file.read(buffer_size)
    return md5.hexdigest()


def get_duplicate_file_paths(folder_path):
    filepaths = get_filepaths_in_folder(folder_path)
    buckets = defaultdict(list)
    for filepath in filepaths:
        with open(filepath, 'rb') as byte_file:
            file_hash = compute_file_hash(byte_file)
        buckets[file_hash].append(filepath)
    return [bucket for bucket in buckets.values() if len(bucket) > 1]


def parse_args(argv):
    parser = ArgumentParser()
    parser.add_argument(
        'folder',
        type=str,
    )
    return parser.parse_args(argv)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    duplicate_filepaths_list = get_duplicate_file_paths(args.folder)
    for duplicate_filepaths in duplicate_filepaths_list:
        print('The following files are duplicates:')
        print(*duplicate_filepaths, sep='\n')
