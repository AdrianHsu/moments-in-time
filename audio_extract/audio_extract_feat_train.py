import numpy as np
import os

import aenet
from aenet import AENet
ae = AENet()

file = open('/tmp3/Moments_in_Time_Mini/audio_mono/path_train.txt', 'r')

save_path = '/tmp3/Moments_in_Time_Mini/audio_extract/training/'
video_path = '/tmp3/Moments_in_Time_Mini/training/'

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


print('len: ' + str(len(wave_files)))
print('load path: done')

txt = open(save_path + 'path_train.txt', 'a')

feat = ae.feat_extract(wave_files, shift=100)
print 'done extract feat!'
print 'feat len: ' + str(len(feat))
for i in range(len(feat)):
    #print feat[i]
    np.save(filenames[i], feat[i])
    category = filenames[i].split('/')[5]
    txt_write = category + ',' + filenames[i] + ',' + video_names[i]
    print txt_write
    txt.write(txt_write)
print 'done'



