import psutil
import os

USER_DIR = os.getenv('HOME')


def teste(path: str, tmp: str) -> str | None:
    for file in os.listdir(path):
        if file.endswith('.txt') and not file.startswith('.'):
            for proc in psutil.process_iter:
                for file in proc.open_files():
                    if file.path == os.path.join(path, file):
                        proc.kill(proc.pid)
            
    
teste(path=USER_DIR, tmp='.sl')