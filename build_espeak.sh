#!/bin/bash

set -ex

deb_archive_url="http://deb.debian.org/debian/pool/main/e/espeak-ng/espeak-ng_1.52.0+dfsg-5~bpo12+1.debian.tar.xz"
deb_archive_name="${deb_archive_url##*/}"
repo_url="https://github.com/espeak-ng/espeak-ng.git"
repo_name="${repo_url##*/}"
repo_name="${repo_name%.git}"

[[ -f $deb_archive_name ]] || wget $deb_archive_url -O $deb_archive_name
if [[ -d deb/$repo_name ]]; then
    (   
        cd $repo_name
        git pull
    )
else
    git clone $repo_url deb/$repo_name
fi
tar -xf $deb_archive_name -C deb/$repo_name

cd deb/$repo_name

for patch in ../../espeak_patches/*.patch; do
    patch -p1 < "$patch"
done

sudo apt-get build-dep -yq .
dpkg-buildpackage -uc -us -b
