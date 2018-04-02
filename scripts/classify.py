"""************************************************************************
PROJECT ENTITY RESOLUTION USING MACHINE LEARNING
	classify.py

This script aims to
1) Classify a message or messages from a file to its author
2) Output "Author Identified" or "Not Author"

************************************************************************"""
def putInFile(featureVec,message):
    presentFeatures = []
    for feature in featureVec.keys():
        if feature in message:
            presentFeatures.append(featureVec[feature]);
    output = "0 "
    for f in sorted(presentFeatures,key=lambda x:int(x)):
        output+=' {}{}'.format(f,":1")
    output +='\n'
    temp.write(output)
    return

import os
import sys

fromtype=sys.argv[1]
featurefile=sys.argv[2]
basepath=os.path.dirname(os.path.abspath(__file__))
if featurefile == "features.txt default location (if exists)":
    featurefile=basepath+'/autogen/features.txt'
modelfile = sys.argv[3]
svmclassify = sys.argv[4]
message = " ".join(sys.argv[5:])
featureVec = {}
#Threshold can be editted to improve precision or recall
#Default is 0
threshold = 0
temp = open(basepath+'/temp.txt','w',encoding='UTF-8')
with open(featurefile, 'r', encoding='UTF-8') as f:
    for line in f:
        line = line.strip().split(" ")
        featureVec[" ".join(line[:-1])] = line[-1]

#temp = open('temp.txt','w',encoding='UTF-8')
#for line in open(featurefile).readlines():
#    line = line.split(" ")
#    featureVec[" ".join(line[:len(line)-1])] = line[len(line)-1].rstrip()

if fromtype=="file":
    data = open(message,'r')
    for dat in data.readlines():
        putInFile(featureVec,dat)
    data.close()
elif fromtype=="message":
    putInFile(featureVec,message)
temp.close()

import subprocess
subprocess.call([svmclassify,basepath+'/temp.txt',modelfile,basepath+'/output.txt'])
temp = open(basepath+'/output.txt','r')
lines = temp.readlines()
temp.close()

os.remove(basepath+'/output.txt')
os.remove(basepath+'/temp.txt')

total = 0
for line in lines:
    total+=float(line.rstrip())
total/=len(lines)
if total > threshold:
    print("Author Identified!")
else:
    print("Not Author")
