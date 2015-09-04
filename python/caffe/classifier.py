#!/usr/bin/env python
"""
Classifier is an image classifier specialization of Net.
"""

import numpy as np

import caffe, os
import time

class Classifier(caffe.Net):
    """
    Classifier extends Net for image class prediction
    by scaling, center cropping, or oversampling.

    Parameters
    ----------
    image_dims : dimensions to scale input for cropping/sampling.
        Default is to scale to net input size for whole-image crop.
    mean, input_scale, raw_scale, channel_swap: params for
        preprocessing options.
    """
    def __init__(self, model_file, pretrained_file, image_dims=None,
                 mean=None, input_scale=None, raw_scale=None,
                 channel_swap=None, forward_time="imc.cpu.openblas.1.forward.csv",
                 layer_time="imc.cpu.openblas.1.layer.csv", app="imc",
                 profile=False, runs=1, warmup=True):

        caffe.Net.__init__(self, model_file, pretrained_file, caffe.TEST)

        # configure pre-processing
        in_ = self.inputs[0]
        self.transformer = caffe.io.Transformer(
            {in_: self.blobs[in_].data.shape})
        self.transformer.set_transpose(in_, (2, 0, 1))
        if mean is not None:
            self.transformer.set_mean(in_, mean)
        if input_scale is not None:
            self.transformer.set_input_scale(in_, input_scale)
        if raw_scale is not None:
            self.transformer.set_raw_scale(in_, raw_scale)
        if channel_swap is not None:
            self.transformer.set_channel_swap(in_, channel_swap)

        self.crop_dims = np.array(self.blobs[in_].data.shape[2:])
        if not image_dims:
            image_dims = self.crop_dims
        self.image_dims = image_dims

        self.app = app
        self.forward_time = forward_time
        self.layer_time = layer_time
        self.profile = profile
        self.runs = runs
        self.warmup = warmup

    def predict(self, inputs):
        """
        Predict classification probabilities of inputs.

        Parameters
        ----------
        inputs : iterable of (H x W x K) input ndarrays.
        oversample : boolean
            average predictions across center, corners, and mirrors
            when True (default). Center-only prediction when False.

        Returns
        -------
        predictions: (N x C) ndarray of class probabilities for N images and C
            classes.
        """
        # Scale to standardize input dimensions.
        input_ = np.zeros((len(inputs),
                           self.image_dims[0],
                           self.image_dims[1],
                           inputs[0].shape[2]),
                          dtype=np.float32)

        if self.app == "imc" or self.app == "dig":
          for ix, in_ in enumerate(inputs):
            input_[ix] = in_

        # Classify
        caffe_in = np.zeros(np.array(input_.shape)[[0, 3, 1, 2]],
                            dtype=np.float32)
        for ix, in_ in enumerate(input_):
            caffe_in[ix] = self.transformer.preprocess(self.inputs[0], in_)


        if self.warmup:
          print "Throwing away first run and returning"
          self.forward_all(**{self.inputs[0]: caffe_in})
          self.warmup = False
          return # hack-city

        if self.profile:
          out = self.forward_all(**{self.inputs[0]: caffe_in})
        else:
          start_fwd = time.time()
          for i in range(0, self.runs):
            out = self.forward_all(**{self.inputs[0]: caffe_in})
          end_fwd = time.time()

          fwd = open(self.forward_time, "a")
          if os.stat(self.forward_time).st_size == 0:
            fwd.write("model,time\n")
          diff = end_fwd - start_fwd
          fwd_time = (diff / float(self.runs))*1000.0

          fwd.write("%s,%.2f\n" % (self.app, float(fwd_time)))
          fwd.close()

        predictions = out[self.outputs[0]]

        return predictions
