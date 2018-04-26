
ROOT='/tmp3/Moments_in_Time_Mini'
VAL_DAT=$ROOT/validation
TRAIN_DAT=$ROOT/training

echo $VAL_DAT

for line in $(find $VAL_DAT); 
do 
    var=$(echo $line | sed "s;validation;audio\/validation;g")
    wav=$(echo $var | sed "s/mp4/wav/g")
    dir=$(echo $wav | cut -d '/' -f1-6)
    mkdir -p $dir
    ffmpeg -i $line $wav
    if [ $? -ne "0" ]; then
        echo 'FAIL,'$wav >> path.txt
    else
        echo 'OK,'$wav >> path.txt
    fi

done
