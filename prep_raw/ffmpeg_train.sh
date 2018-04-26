
ROOT='/tmp3/Moments_in_Time_Raw'
TRAIN_DAT=$ROOT/training

echo $TRAIN_DAT

for line in $(find $TRAIN_DAT); 
do 
    var=$(echo $line | sed "s;training;audio\/training;g")
    wav=$(echo $var | sed "s/mp4/wav/g")
    dir=$(echo $wav | cut -d '/' -f1-6)
    mkdir -p $dir
    ffmpeg -i $line $wav
    if [ $? -ne "0" ]; then
        echo 'FAIL,'$wav >> /tmp3/Moments_in_Time_Raw/audio/path_train.txt
    else
        echo 'OK,'$wav >> /tmp3/Moments_in_Time_Raw/audio/path_train.txt
    fi

done
