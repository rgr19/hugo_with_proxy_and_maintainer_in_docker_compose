#!/bin/bash

githubinit() {

  echo "Do not forget to put ssh pub key to github settings"

  if [ "$#" -lt "2" ]; then
     echo "required [NEWREPO] USER EMAIL"
  fi

  local NEWREPO="$1"
  local USER="$2"
  local EMAIL="$3"

  if [ -z "$NEWREPO" ]; then
    NEWREPO="$PWD"
  fi;

  NEWREPO="$(basename $NEWREPO)"

  echo "Setting up git and github repo=$NEWREPO with USER=$USER EMAIL=$EMAIL"


  git init

  if [ $? -ne 0 ]; then
     echo "ERROR1"
     return $?
  fi

  git config --local user.email "$EMAIL"
  git config --local user.name "$USER"
  git config --local http.proxy ""


  if [ $? -ne 0 ]; then
     echo "ERROR2"
     return $?
  fi

  git lfs install

  if [ $? -ne 0 ]; then
     echo "ERROR3"
     return $?
  fi

  git lfs track "*.a"
  git lfs track "*.so"

  if [ $? -ne 0 ]; then
     echo "ERROR4"
     return $?
  fi

  git add -A
  git commit -m "First commit."
  git remote add origin git@github.com:${USER}/${NEWREPO}.git

  if [ $? -ne 0 ]; then
     echo "ERROR5"
     return $?
  fi

  echo "git remote -v..."
  git remote -v
  echo "git fetch..."
  git fetch
  echo "git pull origin master --allow-unrelated-histories..."
  git pull origin master --allow-unrelated-histories

  echo "git config -l"
  git config --local -l

  echo "git push --set-upstream origin master..."
  git push --set-upstream origin master

}