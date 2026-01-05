#!/bin/bash

set -ex

repo_url="https://github.com/OHF-Voice/piper1-gpl.git"
repo_name="${repo_url##*/}"
repo_name="${repo_name%.git}"

if [[ -d $repo_name ]]; then
    (   
        cd $repo_name
        git pull
    )
else
    git clone $repo_url $repo_name
fi

cd $repo_name

for patch in ../piper_patches/*.patch; do
    patch -p1 < "$patch"
done

[[ -d .venv ]] || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
if command -v nvidia-smi &> /dev/null; then
    pip3 install torch==2.8.0 torchvision --index-url https://download.pytorch.org/whl/cu126
fi
pip3 install --upgrade onnx onnxscript
python3 -m pip install -e .[train]

./build_monotonic_align.sh

python3 setup.py build_ext --inplace
