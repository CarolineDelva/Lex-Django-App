from typing import Union
import os
import hashlib


def get_csci_salt():

    salt = os.environ["CSCI_SALT"]
    return bytes.fromhex(salt)


def hash_str(
        some_val: Union[str, bytes], salt: Union[str, bytes] = "") -> bytes:
    """
    Converts strings to hash digest
    See: https://en.wikipedia.org/wiki/Salt_(cryptography)
    :param some_val: thing to hash, can be str or pybytes
    :param salt: Add randomness to the hashing, can be str or bytes
    :return: sha256 hash digest of some_val with salt, type bytes
    This hash_str function takes input some_val and salt as string or bytes.
    Sha256 from the Hashlib library is assigned to variable m, which is later
    updated with some_val, salt. Both some_val and the salt are encode as
    utf-8 and are casted as strings because bytes cannot be encoded. Lastly,
    the function hash_str returns the hash digest of the salt
    and some_val as bytes.
    """

    m = hashlib.sha256()
    m.update(str(salt).encode("utf-8"))
    m.update(str(some_val).encode())
    return m.digest()


def get_user_id(username: str) -> str:
    salt = get_csci_salt()
    return hash_str(username.lower(), salt=salt).hex()[:8]
