#!/usr/bin/env bash

make -j 4
make distribute
sudo cp distribute/lib/libcaffe.so /usr/local/lib
sudo cp -r distribute/include/caffe /usr/local/include
