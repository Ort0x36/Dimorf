import os


USER_DIR = os.getenv("HOME")
if os.getuid() == 0:
    USER_DIR = '/'

critical_dirs = ['/bin', '/sbin', '/etc', '/lib', '/usr']

for root, dirs, files in os.walk(USER_DIR):
    if '/usr' in root:
        if not root.startswith('/usr/lib'):
            for file in files:
                print(os.path.join(root, file))