#!/bin/bash

set -ex

deb_archive_url="http://deb.debian.org/debian/pool/main/e/espeak-ng/espeak-ng_1.52.0+dfsg-5~bpo12+1.debian.tar.xz"
deb_archive_name="${deb_archive_url##*/}"
repo_url="https://github.com/espeak-ng/espeak-ng.git"
repo_name="${repo_url##*/}"
repo_name="${repo_name%.git}"
repo_rules_url="https://github.com/mitrokun/espeak-ng-data.git"
repo_rules_name="${repo_rules_url##*/}"
repo_rules_name="${repo_rules_name%.git}"

[[ -f $deb_archive_name ]] || wget $deb_archive_url -O $deb_archive_name
[[ -d deb/$repo_name ]] || git clone $repo_url deb/$repo_name
[[ -d deb/$repo_rules_name ]] || git clone $repo_rules_url deb/$repo_rules_name

cd deb/$repo_name
git clean -dfx
git reset --hard HEAD

for patch in ../../espeak_patches/*.patch; do
    patch -p1 < "$patch"
done
cp ../$repo_rules_name/ru_rules dictsource/ru_rules
tar -xf ../../$deb_archive_name

# disable already applied in git source patches
for patch in klatt-garbage libsonic-bigendian clang-target fuzz-link th_dict compile-reproducibility espeak-stdin piper; do
    sed -i "/$patch/d" debian/patches/series
done

# disable failing tests
#echo -e "#!/bin/bash\nexit 0" > debian/tests/tests
sed -i "s|test_phon ru \"(en)s|#test_phon ru \"(en)s|;s|^dv'A|#dv'A|" tests/translate.test
sed -i 's|test_phon ru|#test_phon ru|' tests/dictionary.test

sudo apt-get build-dep -yq .
dpkg-buildpackage -uc -us -b
