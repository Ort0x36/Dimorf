import os


PATH = os.getenv("HOME")

if os.getuid() == 0:
    PATH = '/'
ext_files = ['.txt']
critical_dirs = ['/usr', '/root', '/var']

for root, dirs, files in os.walk(PATH):
    if not root.startswith('/usr') and not(
        root.startswith('/root') and not (
            root.startswith('/var')
        )
    ):
        for file in files:
            print(os.path.join(root, file))

    # for file in files:
    #     end_with_ext = [
    #         ext for ext in ext_files if (
    #             file.endswith(
    #                 ext
    #             ) and not (
    #                 file.startswith('.')
    #             )
    #         )
    #     ]

    #     # # verify file type.
    #     if (end_with_ext):
            
