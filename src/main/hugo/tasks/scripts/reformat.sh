#!/bin/bash


DATE_WITH_TIME=`date "+%Y%m%d-%H%M%S"` #add %3N as we want millisecond too


if [[ -n "$HUGO_BKP" ]]; then
   if [[ $HUGO_BKP -eq 1 ]]; then
			echo "... copy content to backup/content.$DATE_WITH_TIME"
			cp content ../Backup/content.$DATE_WITH_TIME -Rf

			echo "Backing up content to .tgz archives"
			for dirName in $(ls ../Backup | grep -v .tgz); do
			    echo "... backup/${dirName} directory to .tgz archive"
			    (GZIP=-9 tar -czf ../Backup/$dirName.tgz ../Backup/$dirName && rm -Rf ../Backup/$dirName) &
			done
	fi
fi

mkdir -p content/index
mkdir -p content/index/images

# Uses CNAME, RAW_PASSWORD files to fill in config.toml.template and save it as config.toml
# it also uses RAW_PASSWORD to write to HASHED_PASSWORD file and mkdirs _password/<hashed_password>
# that is used for uploads

python config.py

echo "Make dirs with replaced _index by index for index.html"
for i in $(find content -type d | grep _index | sort -f -r); do
    while true; do
        mkdir ${i/_index/index} -p && break || true
    done
done

# _index_imgs="$(find content -type d | grep index | grep images)"
# for i in $_index_imgs; do mv $i ${i/index\//''} || true; done

# in _index.md files replace string _index with index string
echo "In _index.md files replace string _index with index to match index.html"
_index_mds="$(find content -type f | grep index.md | sort -f -r)"
for i in $_index_mds; do
    while true; do
        sed -i 's/_index/index/' $i && break || true
    done
 done

echo "mv content/.../_index/images/* to content/.../images/"
index_imgs="$(find content -type d | grep _index | grep images | sort -f -r)"
for i in $index_imgs; do
    for j in $(find $i -type f | sort -f -r); do
        newpath="${j/_index\//''}"
        if [[ -n "$newpath" ]]; then
            mkdir -p "$(dirname $newpath)"
            echo "mkdir $(dirname $newpath)"
        fi
        if [[ $j != $newpath ]]; then
            mv $j $newpath || true; echo "ERROR: LINE 34 => $j $newpath"
        fi
    done
done

echo "mv content/.../index/images/* to content/.../images/"
index_imgs="$(find content -type d | grep index | grep images | sort -f -r)"
for i in $index_imgs; do
    for j in $(find $i -type f | sort -f -r); do
        newpath="${j/index\//''}"
        if [[ -n "$newpath" ]]; then
            mkdir -p "$(dirname $newpath)"
            echo "mkdir $(dirname $newpath)"
        fi
        if [[ $j != $newpath ]]; then
            mv $j $newpath #|| true; echo "ERROR: LINE 41 => $j $newpath"
        fi
    done
done


echo "mv content/../_index...png to content/.../index...png"
_index_pngs="$(find content -type f | grep -E "_index|index" | grep ".png$" | sort -f -r)"
for i in $_index_pngs; do
    newpath="${i/_index/index}"
    if [[ -n "$newpath" ]]; then
        mkdir -p "$(dirname $newpath)"
    fi
    if [[ $i != $newpath ]]; then
        mv $i $newpath || true; echo "ERROR: LINE 51 => $i $newpath"
    fi
done




# replace spaces with _
# sudo apt install -y rename

PKG_OK=$(dpkg-query -W --showformat='${Status}\n' rename | grep "install ok installed")
echo Checking for rename: $PKG_OK
if [ "" == "$PKG_OK" ]; then
  echo "No rename. Setting up..."
  sudo apt-get --yes install rename
fi

echo "Chalmers study courses case"
find content -depth -name "* *" -execdir rename 's/ /_/g' "{}" \;
find content -depth -name "*\|*" -execdir rename 's/\|/_/g' "{}" \;
find content -depth -name "*7.5_hp*" -execdir rename 's/7.5_hp/_/g' "{}" \;

while [ -n "$(find content | grep __ | grep ".md$" | sort -f -r)" ]; do
    find content -depth -name "*__*" -execdir rename 's/__/_/g' "{}" \;
done

echo "Replace capital names of files with lowercaser... "
for i in $( find ./content | grep -v github | grep -v websites | grep -v literature | sort -f -r ); do
    for n in {1..20}; do
        tmp="$(echo "$i" | tr 'A-Z' 'a-z')"
        if [[ $i != $tmp ]]; then
           mv -f -i "$i" $tmp && break || true
        else
           break
        fi
    done
done



