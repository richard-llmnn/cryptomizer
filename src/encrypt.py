import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad, unpad

default_mode = AES.MODE_GCM


def encrypt_file(binary_data, key, block_size=16):
    # get 256 byte key
    password = hashlib.sha256(key.encode("utf-8")).digest()
    mode = default_mode
    iv = Random.get_random_bytes(16)
    cypher = AES.new(password, mode, iv)

    padded_data = pad(binary_data, block_size)
    encrypted_message = cypher.encrypt(padded_data)
    # prepend the initialization vector to the encrypted file
    return iv + encrypted_message


def decrypt_file(binary_data, key, block_size=16):
    # get 256 byte key
    password = hashlib.sha256(key.encode("utf-8")).digest()
    mode = default_mode
    # the first 16 bytes are the initialization vector
    iv = binary_data[0:16]
    cypher = AES.new(password, mode, iv)
    # after the first 16 bytes the encrypted file starts
    encrypted_message = cypher.decrypt(binary_data[16:])
    try:
        return unpad(encrypted_message, block_size)
    except Exception as exception:
        raise Exception("File could not be decrypted!")
