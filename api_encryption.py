"""
File: api_encryption.py
Author: Martin Lemaire
Date created: November 7, 2023
Description: Encrypts and decrypts API keys.

Modifications:
- [v1.0.0 - 07.11.23 - INITIAL]
"""

"""
Operations Procedure:
 - Save the API keys in a txt file with the key on the first line
   and the secret on the second line
 - Encrypt the file using this code
 - Place the encrypted file on a USB stick
 - Erase the original file
 - When you need to run the code, insert the USB key in the computer
 - When you stop using the code, remove the key

NB : the password is saved in the data.csv of the program, no need to write everytime
"""

# IMPORTS
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os, sys, csv, random, string

def generate_key_and_iv(password, salt):
    """
    Generates key and initialization vector (IV) using the provided password and salt.

    Args:
        password (str): The password for key derivation.
        salt (bytes): A random sequence of bytes used as salt for key derivation.

    Returns:
        bytes: The derived key and IV.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32 + 16,  # Key length + IV length
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key_iv = kdf.derive(password.encode())
    return key_iv[:32], key_iv[32:]

def encrypt_file(file_path, password):
    """
    Encrypts a file using AES encryption.

    Args:
        file_path (str): Path to the file to be encrypted.
        password (str): The password used for encryption.
    """
    with open(file_path, 'rb') as file:
        data = file.read()

    salt = os.urandom(16)
    key, iv = generate_key_and_iv(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()

    with open(file_path + '.encrypted', 'wb') as file:
        file.write(salt + encrypted_data)

def decrypt_file(file_path, password):
    """
    Decrypts an encrypted file.

    Args:
        file_path (str): Path to the encrypted file.
        password (str): The password used for decryption.
    """
    with open(file_path, 'rb') as file:
        salt = file.read(16)
        data = file.read()

    key, iv = generate_key_and_iv(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(data) + decryptor.finalize()

    with open(file_path.replace('.txt.encrypted', '_decrypted.txt'), 'wb') as file:
        file.write(decrypted_data)

# Replace 'file.txt' with your actual file name
file_to_encrypt = sys.argv[1]

if int(sys.argv[2]) == 1:

    # Generate a random password of 100 elements
    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(100))

    encrypt_file(file_to_encrypt, password)

    # Store the password in the csv file
    try:
        with open('data.csv', mode='r') as file:
            reader = csv.reader(file)
            row = next(reader)
            data_csv = [value for value in row]
    except FileNotFoundError: print("The file does not exist. Please check the file path or create the file.")
    except PermissionError: print("Permission denied to open the file. Make sure you have the necessary permissions.")
    except IOError as e: print(f"An I/O error occurred: {e}")
    except Exception as e: print(f"An error occurred: {e}")
    else: pass
    data_csv[15] = password
    try:
        with open('data.csv', mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(data_csv)
    except FileNotFoundError: print("The file does not exist. Please check the file path or create the file.")
    except PermissionError: print("Permission denied to open the file. Make sure you have the necessary permissions.")
    except IOError as e: print(f"An I/O error occurred: {e}")
    except Exception as e: print(f"An error occurred: {e}")
    else: pass

elif int(sys.argv[2]) == 0:

    # Fetch the password stored in the csv file
    try:
        with open('data.csv', mode='r') as file:
            reader = csv.reader(file)
            row = next(reader)
            data_csv = [value for value in row]
    except FileNotFoundError: print("The file does not exist. Please check the file path or create the file.")
    except PermissionError: print("Permission denied to open the file. Make sure you have the necessary permissions.")
    except IOError as e: print(f"An I/O error occurred: {e}")
    except Exception as e: print(f"An error occurred: {e}")
    else: pass

    decrypt_file(file_to_encrypt + '.encrypted', data_csv[15])
