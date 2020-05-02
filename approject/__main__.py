from approject.hash_str import (
    get_csci_salt, hash_str)
from approject.io import atomic_write


def get_user_hash(username, salt=None):
    salt = salt or get_csci_salt()
    return hash_str(username, salt=salt)


if __name__ == "__main__":
    atomic_write()
