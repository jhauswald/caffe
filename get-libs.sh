wget https://google-glog.googlecode.com/files/glog-0.3.3.tar.gz
tar zxvf glog-0.3.3.tar.gz
cd glog-0.3.3
./configure
make && make install

# gflags
wget https://github.com/schuhschuh/gflags/archive/v1.7.tar.gz
tar xzf v1.7.tar.gz
cd gflags-1.7/
export CXXFLAGS="-fPIC" && cmake .. && make VERBOSE=1
./configure
make && make install

# lmdb
git clone git://gitorious.org/mdb/mdb.git
cd mdb/libraries/liblmdb
make && make install

apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev \
libboost-all-dev libhdf5-serial-dev
