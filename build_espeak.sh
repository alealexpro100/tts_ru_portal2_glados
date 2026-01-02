#!/bin/bash

set -ex

deb_archive_url="http://deb.debian.org/debian/pool/main/e/espeak-ng/espeak-ng_1.52.0+dfsg-5~bpo12+1.debian.tar.xz"
deb_archive_name="${deb_archive_url##*/}"
repo_url="https://github.com/espeak-ng/espeak-ng.git"
repo_name="${repo_url##*/}"
repo_name="${repo_name%.git}"

wget $deb_archive_url -O $deb_archive_name
git clone $repo_url
tar -xf $deb_archive_name -C $repo_name

cd $repo_name

for patch in ../espeak_patches/*.patch; do
    echo "Applying patch: $patch"
    git am < "$patch"
done

sudo apt-get build-dep -yq .
dpkg-buildpackage -uc -us -b
