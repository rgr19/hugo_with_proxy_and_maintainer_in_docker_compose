#!/bin/bash -x

conda activate py27_hugo


CWD=$PWD

shopt -s extglob
cd public && rm -v !(".git"|"CNAME"|"."|"..") -Rf
shopt -u extglob

cd $CWD

rm themes/minimus/public -Rf

HUGO_BKP=1 /bin/bash reformat.sh

hugo --gc || true

hugo server \
   --ignoreCache \
   --disableFastRender \
   --verbose \
   --debug \
   --watch

