
ROOT='/tmp3/Moments_in_Time_Mini'
VAL_DAT=$ROOT/validation
TRAIN_DAT=$ROOT/training

echo $VAL_DAT
#find $VAL_DAT -maxdepth 1 #| cut -d "/" -f 1-6 

for line in $(find $VAL_DAT -maxdepth 1); 
do 
    var=$(echo $line | sed "s;validation;audio\/validation;g")
    echo $var
    
done
