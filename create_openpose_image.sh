#!/bin/bash

# Install general dependencies
apt update
apt -y install libprotobuf-dev libleveldb-dev libsnappy-dev \
    libhdf5-serial-dev protobuf-compiler libgflags-dev \
    libgoogle-glog-dev liblmdb-dev libatlas-base-dev \
    libboost-all-dev \
    cmake wget unzip git lsb-release
pip install --upgrade numpy protobuf


# Build and install OpenCV 3
OPENCV_SOURCE_PACKAGE=/root/opencv.zip
EXTRACT_DIR=/root
wget -O ${OPENCV_SOURCE_PACKAGE} https://github.com/opencv/opencv/archive/3.3.0.zip
unzip ${OPENCV_SOURCE_PACKAGE} -d ${EXTRACT_DIR}  
cd ${EXTRACT_DIR}/opencv-3.3.0
mkdir build && cd build
cmake .. -DWITH_CUDA=OFF
make -j4 && make install
rm -Rf .
rm ${OPENCV_SOURCE_PACKAGE}


# Build OpenPose
cd /root && git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose
cd openpose && git checkout 1b0325e
mkdir build && cd build
cmake .. && make -j4
make install

export OPENPOSE_ROOT=/root/openpose

# Buuild PyOpenPose
cd /root && git clone https://github.com/FORTH-ModelBasedTracker/PyOpenPose && cd PyOpenPose
git checkout 538dfea9
mkdir build && cd build
cmake  .. -DPYTHON_INCLUDE_DIR="/usr/include/python2.7;/usr/local/lib/python2.7/dist-packages/numpy/core/include"
make && make install
ln -s /usr/local/lib/PyOpenPose.so /usr/lib/python2.7/

ldconfig

# Cleanup. Important : lsb-release has python3.5 as a requirement, but it is needed to build openpose
# TODO: Remove these requirements from the build process, if possible
apt -y purge lsb-release cmake unzip wget
apt -y autoremove
