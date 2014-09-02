## Caffe ported to run native on Xeon Phi
The Caffe source code here is outdated. You should use the current version from here:
https://github.com/BVLC/caffe

#### Instructions:
See the Makefile and Makefile.config from here to compile for Xeon Phi
https://github.com/ivankreso/caffe-xeon-phi/blob/master/Makefile
https://github.com/ivankreso/caffe-xeon-phi/blob/master/Makefile.conf

You will also need to cross-compile all the Caffe dependencies for Xeon Phi.
Library sources and cross-compilation flags used are here:  
https://github.com/ivankreso/caffe-deps-xeon-phi

One library (Protobuf) needs to be patched first so you can use already patched source from the repository or
if you want to apply the patch to Protobuf yourself you can find it here:  
https://github.com/ivankreso/caffe-deps-xeon-phi/blob/master/protobuf-2.5.0/atomicops_internals_x86_gcc.h.patch

