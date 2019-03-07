sourceDat=$1
tarFolder=$2
remark1=$3
remark2=$4
sourceDatName=`echo ${sourceDat}|rev|cut -d '/' -f 1|rev`
if [ ${remark1}c == c ];then
	remark1='defaultRemark'
fi
if [ ${remark2}c == c ];then
	remark2='defaultRemark'
fi
awk '{printf("%s\t%s\t%s\n",$0,remark1,remark2)}' remark1=$remark1 remark2=$remark2 ${sourceDat}  > ${tarFolder}/relSet.dat
echo 'add remark complete'
