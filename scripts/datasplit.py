"""************************************************************************
PROJECT ENTITY RESOLUTION USING MACHINE LEARNING
	datasplit.py

This script aims to
1) Sort a train.txt and test.txt file to make it for a specific author so as to be able to use it for training and testing

************************************************************************"""
import sys
class DataSplit:
    def __init__(self,fileName):
        self.name = fileName
    def classifyFile(self,newFileName,authorNum):
        import re
        f = open(self.name, 'r+')
        nf = open(newFileName, 'w')
#Substitude the start of every line (author number) for +1 or -1 respectively
        for line in f:
            matches = re.findall(r'^{0}'.format(authorNum),line)
            if len(matches)>0:
                result = re.sub(r'^[0-9]+','+1',line)
            else:
                result = re.sub(r'^[0-9]+','-1',line)
            nf.write(result)
        f.close()
        nf.close()
        
