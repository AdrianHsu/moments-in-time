# Copyright 2017 The TensorFlow Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

r"""A simple demonstration of running VGGish in inference mode.

This is intended as a toy example that demonstrates how the various building
blocks (feature extraction, model definition and loading, postprocessing) work
together in an inference context.

A WAV file (assumed to contain signed 16-bit PCM samples) is read in, converted
into log mel spectrogram examples, fed into VGGish, the raw embedding output is
whitened and quantized, and the postprocessed embeddings are optionally written
in a SequenceExample to a TFRecord file (using the same format as the embedding
features released in AudioSet).

Usage:
  # Run a WAV file through the model and print the embeddings. The model
  # checkpoint is loaded from vggish_model.ckpt and the PCA parameters are
  # loaded from vggish_pca_params.npz in the current directory.
  $ python vggish_inference_demo.py --wav_file /path/to/a/wav/file

  # Run a WAV file through the model and also write the embeddings to
  # a TFRecord file. The model checkpoint and PCA parameters are explicitly
  # passed in as well.
  $ python vggish_inference_demo.py --wav_file /path/to/a/wav/file \
                                    --tfrecord_file /path/to/tfrecord/file \
                                    --checkpoint /path/to/model/checkpoint \
                                    --pca_params /path/to/pca/params

  # Run a built-in input (a sine wav) through the model and print the
  # embeddings. Associated model files are read from the current directory.
  $ python vggish_inference_demo.py
"""

from __future__ import print_function

import numpy as np
from scipy.io import wavfile
import six
import tensorflow as tf

import vggish_input
import vggish_params
import vggish_postprocess
import vggish_slim

flags = tf.app.flags

flags.DEFINE_string(
    'wav_file', None,
    'Path to a wav file. Should contain signed 16-bit PCM samples. '
    'If none is provided, a synthetic sound is used.')

flags.DEFINE_string(
    'checkpoint', 'vggish_model.ckpt',
    'Path to the VGGish checkpoint file.')

flags.DEFINE_string(
    'pca_params', 'vggish_pca_params.npz',
    'Path to the VGGish PCA parameters file.')

flags.DEFINE_string(
    'tfrecord_file', None,
    'Path to a TFRecord file where embeddings will be written.')

FLAGS = flags.FLAGS


def main(_):

  file = open('/tmp3/Moments_in_Time_Mini/audio_mono/path_val.txt', 'r')

  save_path = '/tmp3/Moments_in_Time_Mini/audio_vggish/validation/'
  video_path = '/tmp3/Moments_in_Time_Mini/validation/'

  wave_files = []
  filenames = []
  video_names = []
  for line in file.readlines():
      
      spl = line.split(',')
      if spl[0] == 'FAIL':
          continue
      
      path = spl[1]
      wave_files.append(path)
      # steering/yt-q39BHbYrufQ_45.wav
      mydir = path.split('/')[-2]
      if not os.path.exists(save_path + mydir):
          print('mkdir: ' + save_path + mydir)
          os.makedirs(save_path + mydir)
      f = save_path + mydir + '/' + path.split('/')[-1] + '.npy'
      #print f
      filenames.append(f)
      # video path
      v_path = spl[2]
      v = video_path + mydir + '/' + v_path.split('/')[-1]
      #print v
      video_names.append(v)

  print(len(filenames))
  print(len(video_names))

  print('len: ' + str(len(wave_files)))
  print('load path: done')

  txt = open(save_path + 'path_val.txt', 'a')

  for i in range(len(wave_files)):
    examples_batch = vggish_input.wavfile_to_examples(wav_files[i])
    # print(examples_batch.shape) # (3, 96, 64)

    # Prepare a postprocessor to munge the model embeddings.
    pproc = vggish_postprocess.Postprocessor(FLAGS.pca_params)

    # If needed, prepare a record writer to store the postprocessed embeddings.
    writer = tf.python_io.TFRecordWriter(
        FLAGS.tfrecord_file) if FLAGS.tfrecord_file else None

    with tf.Graph().as_default(), tf.Session() as sess:
      # Define the model in inference mode, load the checkpoint, and
      # locate input and output tensors.
      vggish_slim.define_vggish_slim(training=False)
      vggish_slim.load_vggish_slim_checkpoint(sess, FLAGS.checkpoint)
      features_tensor = sess.graph.get_tensor_by_name(
          vggish_params.INPUT_TENSOR_NAME)
      embedding_tensor = sess.graph.get_tensor_by_name(
          vggish_params.OUTPUT_TENSOR_NAME)

      # Run inference and postprocessing.
      [embedding_batch] = sess.run([embedding_tensor],
                                   feed_dict={features_tensor: examples_batch})
      # print(embedding_batch.shape) # (3, 128)
      feat = pproc.postprocess(embedding_batch)
      # print(postprocessed_batch.shape) #(3, 128) 

      np.save(filenames[i], feat)
      category = filenames[i].split('/')[5]
      txt_write = category + ',' + filenames[i] + ',' + video_names[i]
      print txt_write
      txt.write(txt_write)

  if writer:
    writer.close()

if __name__ == '__main__':
  tf.app.run()
