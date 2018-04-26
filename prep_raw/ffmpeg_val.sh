
ROOT='/tmp3/Moments_in_Time_Raw'
VAL_DAT=$ROOT/validation

echo $VAL_DAT

for line in $(find $VAL_DAT); 
do 
    var=$(echo $line | sed "s;validation;audio\/validation;g")
    wav=$(echo $var | sed "s/mp4/wav/g")
    dir=$(echo $wav | cut -d '/' -f1-6)
    mkdir -p $dir
    ffmpeg -i $line $wav
    if [ $? -ne "0" ]; then
        echo 'FAIL,'$wav >> /tmp3/Moments_in_Time_Raw/audio/path_val.txt
    else
        echo 'OK,'$wav >> /tmp3/Moments_in_Time_Raw/audio/path_val.txt
    fi

done
