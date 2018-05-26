import numpy as np
import os

import aenet
from aenet import AENet
ae = AENet()

# wc -l
# 20001 path_test.txt

file = open('/tmp3/Moments_in_Time_Mini/audio_mono_test/path_test.txt', 'r')

save_path = '/tmp3/Moments_in_Time_Mini/audio_extract/testing/'
video_path = '/tmp3/Moments_in_Time_Mini/momentsMiniTest/'

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
    #mydir = path.split('/')[-2]
    #if not os.path.exists(save_path + mydir):
    #    print('mkdir: ' + save_path + mydir)
    #    os.makedirs(save_path + mydir)
    f = save_path + path.split('/')[-1] + '.npy'
    print f # /tmp3/Moments_in_Time_Mini/audio_extract/testing/39987.wav.npy
    filenames.append(f)
    # video path
    v_path = spl[2]
    v = video_path + v_path.split('/')[-1]
    print v # /tmp3/Moments_in_Time_Mini/momentsMiniTest/39987.mp4
    video_names.append(v)


print(len(wave_files)) # total: 12776/20001
print(len(filenames))
print(len(video_names))

txt = open(save_path + 'path_test.txt', 'a')
batch_size = 50
cnt = 0
while cnt < 12776:
    if cnt == 12750:
        batch_size = 26
    
    print(cnt)
    print(cnt + batch_size)
    wave_files_batch = wave_files[cnt:cnt+batch_size]
    filenames_batch = filenames[cnt:cnt+batch_size]
    video_names_batch = video_names[cnt:cnt+batch_size]

    print('len: ' + str(len(wave_files_batch)))
    print('load path: done')

    #exit(0)

    feat = ae.feat_extract(wave_files_batch, shift=100)
    print 'done extract feat!'
    print 'feat len: ' + str(len(feat))
    for i in range(len(feat)):
        #print feat[i]
        np.save(filenames_batch[i], feat[i])
        category = filenames_batch[i].split('/')[5]
        txt_write = category + ',' + filenames_batch[i] + ',' + video_names_batch[i]
        print txt_write
        txt.write(txt_write)
    print 'done'
    
    cnt += batch_size


