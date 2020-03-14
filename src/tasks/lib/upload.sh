#!/bin/bash

# If a command fails then the deploy stops
set -e


printf "\033[0;32mDeploying updates to GitHub...\033[0m\n"

CWD=$PWD

shopt -s extglob
cd public && rm -v !(".git"|"CNAME"|"."|"..") -Rf
shopt -u extglob

# Add changes to git.
git add .

# Commit changes.
msg="cleaning site $(date)"
if [ -n "$*" ]; then
	msg="$*"
fi

git commit -m "$msg" || true

# Push source and build reposList.
git push origin master || true

cd $CWD

/bin/bash reformat.sh || true

HASHED_PASSWORD="$(cat PASSWORD_HASHED)"

# Build the project.
hugo --gc || true

# hide under hash of password
## clean old content
rm _password/$HASHED_PASSWORD/* -Rf
## move static site under hash
mv public/* _password/$HASHED_PASSWORD -f
## copy hashed static site to github repo public
cp _password/* public -Rf
## copy domain name file to hashed static site
cp CNAME public -Rf

# Go to hashed static website
cd public

# Add changes to git
git add .

# Commit changes
msg="rebuilding site $(date)"
if [ -n "$*" ]; then
	msg="$*"
fi
git commit -m "$msg"

# Push source and build reposList
git push origin master
