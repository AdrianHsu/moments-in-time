
# /tmp3/Moments_in_Time_Mini/momentsMiniTest

ROOT='/tmp3/Moments_in_Time_Mini'
TEST_DAT=$ROOT/momentsMiniTest

echo $VAL_DAT
mkdir -p $ROOT/audio_mono_test
for line in $(find $TEST_DAT); 
do 
    var=$(echo $line | sed "s;momentsMiniTest;audio_mono_test;g")
    wav=$(echo $var | sed "s/mp4/wav/g")
    
    ffmpeg -i $line -c pcm_s16le -ac 1 -ar 16000 $wav
    if [ $? -ne "0" ]; then
        echo 'FAIL,'$wav','$line >> /tmp3/Moments_in_Time_Mini/audio_mono_test/path_test.txt
    else
        echo 'OK,'$wav','$line >> /tmp3/Moments_in_Time_Mini/audio_mono_test/path_test.txt
    fi

done
