#!/usr/bin/python

import hashlib
import sys
import os
import shutil

def get_hashed_password(rawPassword):
    hashed = hashlib.sha1(rawPassword).hexdigest()
    return hashed


def setup_dir_hashed_password(hashedPassword):
    passwordDirPath = os.path.join("_password", hashedPassword)
    if os.path.exists(passwordDirPath):
        shutil.rmtree(passwordDirPath)
    os.makedirs("_password/" + hashedPassword)

def save_hashed_password(hashedPassword):
    with open("HASHED_PASSWORD", "w") as fp:
        fp.write(hashedPassword)

def password_setup(rawPassword):
    hashedPassword = get_hashed_password(rawPassword)
    setup_dir_hashed_password(hashedPassword)
    save_hashed_password(hashedPassword)
    return hashedPassword

if __name__ == '__main__':
    _, rawPassword = sys.argv
    password_setup(rawPassword)
