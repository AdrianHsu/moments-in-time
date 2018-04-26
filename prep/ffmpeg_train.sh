
ROOT='/tmp3/Moments_in_Time_Mini'
VAL_DAT=$ROOT/validation
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
        echo 'FAIL,'$wav >> path_train.txt
    else
        echo 'OK,'$wav >> path_train.txt
    fi

done
