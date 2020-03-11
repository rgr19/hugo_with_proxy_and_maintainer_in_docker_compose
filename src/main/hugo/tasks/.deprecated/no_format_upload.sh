#!/bin/bash

# If a command fails then the deploy stops
set -e


printf "\033[0;32mDeploying updates to GitHub...\033[0m\n"

CWD=$PWD
HASHED_PASSWORD="$(cat PASSWORD_HASHED)"

############################################################
#### Clean and push
############################################################

rm public -Rf
# hide under hash of password
## clean old content
if [ ! -z "$HASHED_PASSWORD" ]; then
if [ -d "private/$HASHED_PASSWORD" ]; then
	rm private/$HASHED_PASSWORD/* -Rf
fi
fi

mkdir -p private/$HASHED_PASSWORD

cd private

# Add changes to git.
git add .

# Commit changes.
msg="Cleaning site at $(date)"
if [ -n "$*" ]; then
	msg="$*"
fi

git commit -m "$msg" || true

# Push source and build repos.
git push origin master || true


############################################################
#### Rebuild and push
############################################################


cd $CWD

# Build the project.
hugo --gc || true

## move static site under hash
mv public/* private/$HASHED_PASSWORD -f
cp CNAME private

# Go to hashed static website
cd private

# Add changes to git
git add .

# Commit changes
msg="Rebuilding site at $(date)"
if [ -n "$*" ]; then
	msg="$*"
fi
git commit -m "$msg"

# Push source and build repos
git push origin master
