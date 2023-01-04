import os

critical = ['/usr', '/var', '/lib']
for sub in critical:
    print(sub)
    for root, dirs, files in os.walk('/'):
        if not root.startswith(sub):
            print(root)