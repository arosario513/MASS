#!/bin/bash
set -e
mkdir -p mass
cd mass
git init
git branch -m main
git remote add origin https://github.com/arosario513/COMP-2052.git
git sparse-checkout init --cone
git sparse-checkout set work/final
git pull origin main
mv ./work/final ../final
cd ..
rm -rf mass
