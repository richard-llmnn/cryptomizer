import hashlib
import os.path
import string

from random import sample
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad, unpad
from typing import Any

DEFAULT_MODE = AES.MODE_GCM
ENCRYPTED_FILE_ENDING = ".crypt"


def encrypt_file(binary_data: Any, key: str, block_size: int = 16) -> Any:
    # get 256 byte key
    password = hashlib.sha256(key.encode("utf-8")).digest()
    mode = DEFAULT_MODE
    iv = Random.get_random_bytes(16)
    cypher = AES.new(password, mode, iv)

    padded_data = pad(binary_data, block_size)
    encrypted_message = cypher.encrypt(padded_data)
    # prepend the initialization vector to the encrypted file
    return iv + encrypted_message


def decrypt_file(binary_data: Any, key: str, block_size: int = 16) -> Any:
    # get 256 byte key
    password = hashlib.sha256(key.encode("utf-8")).digest()
    mode = DEFAULT_MODE
    # the first 16 bytes are the initialization vector
    iv = binary_data[0:16]
    cypher = AES.new(password, mode, iv)
    # after the first 16 bytes the encrypted file starts
    encrypted_message = cypher.decrypt(binary_data[16:])
    try:
        return unpad(encrypted_message, block_size)
    except Exception as exception:
        raise Exception("File could not be decrypted!")


def encrypt_files_by_path(file_paths: list[str], output_folder: str, password: str) -> None:
    for file_path in file_paths:
        if not os.path.isabs(file_path):
            raise Exception("File could not be opened!")

        with open(file_path, "rb") as input_file:
            filename = os.path.split(file_path)[1]

            with open(os.path.join(output_folder, filename + ENCRYPTED_FILE_ENDING), "wb") as output_file:
                output_file.write(encrypt_file(input_file.read(), password))


def decrypt_files_by_path(file_paths: list[str], output_folder: str, password: str) -> None:
    for file_path in file_paths:
        if not os.path.isabs(file_path):
            raise Exception("File could not be opened!")

        with open(file_path, "rb") as input_file:
            filename = os.path.split(file_path)[1]

            if ENCRYPTED_FILE_ENDING not in filename:
                raise Exception(f"The given file {file_path} is not an encrypted file!")
            # remove the ".crypt" from the file
            filename = filename.removesuffix(ENCRYPTED_FILE_ENDING)

            with open(os.path.join(output_folder, filename), "wb") as output_file:
                output_file.write(decrypt_file(input_file.read(), password))


# Warning, the generated password is not cryptographically secure!
def generate_password(length: int) -> str:
    password_as_list = sample(string.ascii_letters + string.digits, length)
    return ''.join(str(char) for char in password_as_list)
