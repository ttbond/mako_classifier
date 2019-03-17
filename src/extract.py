import sys
import re
import io
import os
import math
import argparse
from collections import defaultdict
parser=argparse.ArgumentParser()
parser.add_argument('sourceFile')
parser.add_argument('tarFolder')
parser.add_argument('-d','--depth',default=10,type=int)
args=parser.parse_args()
tarFolder=args.tarFolder
sourceFile=open(tarFolder+"/relSet.dat")
relFile=open(tarFolder+"/relSet2.dat","w")
id=1
while True:
    tmpStr=sourceFile.readline()
    if tmpStr=='':
        break
    tmpStr=tmpStr.split('\n')[0]
    tmpStr=tmpStr.split("\t")
    relStr=''+tmpStr[0]+'\t'+tmpStr[1]+'\t'+tmpStr[2]+'\t'+tmpStr[5].split('\n')[0]+'\t'
    details=tmpStr[6]
    tmpStr=tmpStr[4].split(';')
    flag = False
    for strs in tmpStr:
        sonStr = strs.split("=")
        if sonStr[0] == "Pattern":
            relStr = relStr + sonStr[1].split('\n')[0] + '\t'
            flag = True
    if flag == False:
        print(id, "Pattern error")
        exit()
    flag=False
    for strs in tmpStr:
        sonStr=strs.split("=")
        if sonStr[0]=="Ori":
            relStr=relStr+sonStr[1].split('\n')[0]+'\t'
            flag=True
    if flag==False:
        print(id,"Ori error")
        exit()
    relStr=relStr+details
    print(relStr,file=relFile)
    id+=1
sourceFile.close()
relFile.close()

maxPatternLen=15
print("check data format complete")
class mySv():
    types=defaultdict(int)
    typesId=1
    svTyp=defaultdict(int)
    svTypId=1
    def __init__(self,tmpstr='',myid=''):
        if tmpstr=='':
            return
        li=tmpstr.split("\t")
        self.chr=li[0]
        if self.chr[0]=='c':
            self.chr=self.chr[3:]
        if self.chr=='X' or self.chr=='x':
            self.chr=23
        elif self.chr=='Y' or self.chr=='y':
            self.chr=24
        self.chr=int(self.chr)
        self.st=int(li[1])
        self.ed=int(li[2])
        if self.svTyp[li[3]]==0:
            self.addSvTyp(li[3])
        self.sv=self.svTyp[li[3]]
        li2=li[4].split(",")
        self.seq_type=[]
        self.seq_dis=self.ed-self.st+1
        self.seq_positive=[]
        self.seq_negative=[]
        self.seq_flag=[]
        self.id=myid
        appearNum=defaultdict(int)
        self.ent=0
        for i in range(0,len(li2)):
            tli2=li2[i].split('<')
            for j in range(1,len(tli2)):
                tli2[j]=tli2[j].split('>')[1]
            for j in range(len(tli2)):
                if self.types[tli2[j]]==0:
                    self.addtype(tli2[j])
                self.seq_type.append(self.types[tli2[j]])
        self.defLen=0
        for i in range(len(self.seq_type)):
            appearNum[self.seq_type[i]]+=1
            if appearNum[self.seq_type[i]]==1:
                self.defLen+=1
        for i in range(1,10):
            if appearNum[i]>0:
                self.ent-=float(appearNum[i])/len(self.seq_type)*math.log(float(appearNum[i])/len(self.seq_type),2)
        arpNum=0
        for i in range(1,10):
            if i==1 or i==2 or i==5:
                continue
            if appearNum[i]>0:
                arpNum+=1
        #self.ent+=1
        self.ent*=arpNum
        li2=li[5].split(",")
        for i in range(0,len(li2)):
            self.seq_positive.append(int(li2[i].split("+")[0]))
            self.seq_negative.append(int(li2[i].split("+")[1][:-1]))
    #[.0. id] [.1. 4 features of the 1st pattern] [.5. 3 features of the following 14 patterns]
    #[.47. total pattern num] [.48. svType] [.49. chr] [.50. stPos] [.51. edPos] [.52. entropy]
    def printme(self):
        rel=str(self.id)+' '
        findflag=0
        for i in range(0,len(self.seq_type)):
            tmpflag=0
            if self.seq_positive[i]>self.seq_negative[i]:
                tmpflag=1
            elif self.seq_positive[i]<self.seq_negative[i]:
                tmpflag=2
            if tmpflag>0 and findflag==0:
                for j in range(0,i):
                    self.seq_flag[j]=tmpflag
            if tmpflag>0:
                findflag=tmpflag
                self.seq_flag.append(tmpflag)
            else:
                self.seq_flag.append(findflag)
        for i in range(0,maxPatternLen):
            if i<len(self.seq_type):
                if i==0:
                    rel=rel+str(self.seq_type[i])+' '+str(self.ed-self.st)+' '+str(self.seq_flag[i])+' '+str(self.seq_negative[i]+self.seq_positive[i])+' '
                else:
                    rel=rel+str(self.seq_type[i])+' '+str(self.seq_flag[i])+' '+str(self.seq_negative[i]+self.seq_positive[i])+' '
            else:
                rel=rel+"0 0 0 "
        rel=rel+' '+str(self.defLen)+' '+str(self.sv)+' '+str(self.chr)+' '+str(self.st)+' '+str(self.ed)
        rel=rel+' '+str(self.ent)
        return rel
    @classmethod
    def addtype(cls,tmpstr):
        cls.types[tmpstr]=cls.typesId
        cls.typesId=cls.typesId+1
    @classmethod
    def addSvTyp(cls,tmpstr):
        cls.svTyp[tmpstr]=cls.svTypId
        cls.svTypId=cls.svTypId+1
    @classmethod
    def initDict(cls):
        if os.path.exists('typeId.dat'):
            with open('typeId.dat') as typIdF:
                for tmpStr in typIdF.readlines():
                    tmpStr=tmpStr.split('\n')[0]
                    ttyp=tmpStr.split(' ')[0]
                    ttypId=int(tmpStr.split(' ')[1])
                    cls.types[ttyp]=ttypId
                    cls.typesId=max(ttypId+1,cls.typesId)
    @classmethod
    def recordDict(cls):
        with open('typeId.dat','w') as typIdF:
            for typ in cls.types:
                print(typ,cls.types[typ],file=typIdF)


sourceFile=open(tarFolder+"/relSet2.dat")
relFile=open(tarFolder+"/relSet3.dat","w")
myid=0
tmpSv=mySv()
tmpSv.initDict()
while True:
    tmpstr=sourceFile.readline()
    if tmpstr=='':
        break
    if tmpstr.split('\t')[2]=='-':
        continue
    myid=myid+1
    tmpMySv=mySv(tmpstr,myid)
    print(tmpMySv.printme(),file=relFile)

tmpSv.recordDict()
sourceFile.close()
relFile.close()
print("convert complete")
