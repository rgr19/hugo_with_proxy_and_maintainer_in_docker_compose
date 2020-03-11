#!/bin/bash

# This script shall be executed after creating github repository
# to connect it to local git repo

source githubinit.sh

EMAIL="onceawaken@outlook.com"
USER="rgr19"
NEWREPO_PATH="$PWD"

githubinit "$NEWREPO_PATH" $USER $EMAIL
git submodule add git@github.com:$USER/$USER.github.io.git public
git submodule add -b master git@github.com:$USER/$USER.github.io.git public
