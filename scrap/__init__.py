import os
import sys
from os import path

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'setup_log.conf')

if __name__ == '__main__':
    print('> ', parent_dir_path)
    print('> ', log_file_path)
