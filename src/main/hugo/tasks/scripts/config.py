#!/usr/bin/python

import os
import sys
from password_generator import password_setup


CNAME = "example.com"
HASHED_PASSWORD = ""

with open("CNAME", "r") as fp:
    CNAME = fp.read()

WEBSITE = "https://www." + CNAME

if os.path.exists("PASSWORD_HASHED"):
    with open("PASSWORD_HASHED", "r") as fp:
        HASHED_PASSWORD = fp.read()

else:
    RAW_PASSWORD = ""
    with open("PASSWORD_RAW", "r") as fp:
        RAW_PASSWORD = fp.read().strip()

    if not RAW_PASSWORD:
        raise ValueError("RAW_PASSWORD file can not be empty.")

    HASHED_PASSWORD = password_setup(RAW_PASSWORD)

with open("IGNORED_FILES", "r") as fp:
    IGNORED_FILES = fp.read()

with open("config.toml.template", "r") as fp:
    template = fp.read()

config = template.format(website=WEBSITE,
                         hashed_password=HASHED_PASSWORD,
                         ignored_files=IGNORED_FILES)

with open("config.toml", "w") as fp:
    fp.write(config)
