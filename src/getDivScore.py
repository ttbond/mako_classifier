from keras import backend
from keras.models import load_model
import numpy as np
import math
from collections import defaultdict
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('sourceFile')
parser.add_argument('tarFolder')
parser.add_argument('-o','--output',default='None')
parser.add_argument('-d','--depth',default=10,type=int)
args=parser.parse_args()
tarFolder=args.tarFolder
relFileName=args.output
sourceFile=args.sourceFile
if relFileName=='None':
    relFileName=tarFolder+'/'+sourceFile.split('/')[-1][:-4]+'.withScore.vcf'
else:
    relFileName=tarFolder+'/'+relFileName+'.vcf'
myData=np.loadtxt(tarFolder+"/relSet3.dat")
#tmpZero is to compulsarily extend the last time's feature
tmpZero=np.zeros((np.shape(myData)[0],2),dtype=np.float)
#ten time noedes and one length node
X=myData[:,[1]+list(range(3,32))]
X=np.hstack((X,myData[:,[2]],tmpZero))
#label
y=myData[:,[48,49,50,51]]
label=myData[:,[48]]
#the model need the label start from 0
X=X.reshape(np.shape(X)[0],11,3)
model=load_model('model/simuModel.h5')
nowRel=model.predict_classes(X)
scoreRel=list()
for i in range(np.shape(nowRel)[0]):
    scoreRel.append(myData[i,47]*float(myData[i,52])+1)
scoreRel=np.array(scoreRel)
outRel=np.hstack((np.reshape(nowRel,(np.shape(nowRel)[0],1)),
                  np.reshape(scoreRel,(np.shape(scoreRel)[0],1))))
outSvString=list(("DEL","DUP","INV"))
with open(relFileName,'w') as relF, open(sourceFile) as srcF:
    for i in range(np.shape(outRel)[0]):
        prefix=srcF.readline()
        prefix=prefix.split('\n')[0]
        print(prefix,end=';',file=relF)
        for j in range(np.shape(outRel)[1]):
            if j==0:
                print("SVTYPE=%s"%(outSvString[int(outRel[i,j])]),end=';',file=relF)
            else:
                print("CX=%.3f"%(outRel[i,j]),file=relF)
