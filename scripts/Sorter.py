"""************************************************************************
PROJECT ENTITY RESOLUTION USING MACHINE LEARNING
	Sorter.py

This script aims to
1) Sort a train.txt and test.txt file to make it for a specific author so as to be able to use it for training and testing

************************************************************************"""
import sys
import os
aut = sys.argv[1]
folder = sys.argv[2]
if len(sys.argv) > 3:
    fileNameTest=sys.argv[3]
    fileNameTrain = sys.argv[4]
else:
	fileNameTest = None
	fileNameTrain = None
if fileNameTest is None or fileNameTest == "test.txt default location (if exists)":
    fileNameTest = os.path.dirname(__file__)+'/autogen/test.txt'
if fileNameTrain is None or fileNameTrain == "train.txt default location (if exists)":
    fileNameTrain = os.path.dirname(__file__)+'/autogen/train.txt'
basepath=os.path.dirname(os.path.abspath(__file__))
#Functions from the datasplit.py file is used
import datasplit
dataSplitTest = datasplit.DataSplit(fileNameTest)
dataSplitTrain = datasplit.DataSplit(fileNameTrain)
fNameTest = folder+'/test'+str(aut)+'.txt'
fNameTrain = folder+'/train'+str(aut)+'.txt'
dataSplitTest.classifyFile(fNameTest,aut)
dataSplitTrain.classifyFile(fNameTrain,aut)
print('success')
