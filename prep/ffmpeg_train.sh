
ROOT='/tmp3/Moments_in_Time_Mini'
TRAIN_DAT=$ROOT/training

echo $TRAIN_DAT

for line in $(find $TRAIN_DAT); 
do 
    var=$(echo $line | sed "s;training;audio_mono\/training;g")
    wav=$(echo $var | sed "s/mp4/wav/g")
    dir=$(echo $wav | cut -d '/' -f1-6)
    mkdir -p $dir
    ffmpeg -i $line -c pcm_s16le -ac 1 -ar 16000 $wav
    if [ $? -ne "0" ]; then
        echo 'FAIL,'$wav','$line >> /tmp3/Moments_in_Time_Mini/audio_mono/path_train.txt
    else
        echo 'OK,'$wav','$line >> /tmp3/Moments_in_Time_Mini/audio_mono/path_train.txt
    fi

done
