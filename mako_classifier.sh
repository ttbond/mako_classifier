bash src/addRemark.sh $1 $2
python3 src/extract.py $1 $2
python3 src/getDivScore.py $1 $2 $3
