"""************************************************************************
PROJECT ENTITY RESOLUTION USING MACHINE LEARNING
	xmlparser.py

This script aims to
1) parse the xml data corpus
2) convert files to feature vector format
other useful files will also be in the output of this script

Run with command line arguments: Location of XML corpus, 
								 Sort Type ('Space'/'Bigram' etc.)
************************************************************************"""
import xml.etree.ElementTree as ET
import sys
import os
import filesplit
#Initialize variables
corpus = sys.argv[1]
sortType = sys.argv[2]
tree = ET.parse(corpus)
root = tree.getroot()
authorList = {}
authorFreq = {}
counter = 1
messageList=[]
basepath=os.path.dirname(os.path.abspath(__file__))
if not os.path.isdir(basepath+'/autogen'):
    os.makedirs(basepath+'/autogen')	
msgFile = open(basepath+'/autogen/messages.txt','w',encoding='UTF-8')
autFile = open(basepath+'/autogen/authors.txt','w',encoding='UTF-8')
autFreqFile = open(basepath+'/autogen/authorFreq.txt','w',encoding='UTF-8')
for message in root:
#Obtain list of authors and also the frequency of occurance for each author output in authors.txt and authorFreq.txt respectively
    if message[1][0].text not in authorList.keys():
        authorList[message[1][0].text]=counter
        authorFreq[message[1][0].text]=1
        counter+=1
    else:
        authorFreq[message[1][0].text]+=1
#Get a list of authors and their messages which will be output in messages.txt
    messageList.append(str(authorList[message[1][0].text])+" "+message[0].text)
for message in messageList:
    msgFile.write('{} \n'.format(message))
for author,number in sorted(authorList.items(), key=lambda x:x[1]):
    autFile.write('{} {}\n'.format(number,author))
for author,freq in sorted(authorFreq.items(), key=lambda x:x[1]):
    autFreqFile.write('Author:{} Frequency:{}\n'.format(authorList[author],freq))
msgFile.close()
autFile.close()
autFreqFile.close()
#Create feature vectors according to types specified
#FULL LIST OF SORT TYPES: Space, Bigram, Trigram, 4gram, WordUnigram, WordBigram, WordTrigram,
#CharWordBigram, CharTrigramWordUnigram, Char4gramWordUnigram, CharBigramWordUnigram
if sortType=="Space":
    flist=filesplit.splitDataBySpace(messageList)
elif sortType=="Bigram":
    flist=filesplit.splitDataByNGrams(messageList,2)
elif sortType=="Trigram":
    flist=filesplit.splitDataByNGrams(messageList,3)
elif sortType=="4gram":
    flist=filesplit.splitDataByNGrams(messageList,4)
elif sortType=="WordUnigram":
    flist=filesplit.splitDataByWordNGrams(messageList,1)
elif sortType=="WordBigram":
    flist=filesplit.splitDataByWordNGrams(messageList,2)
elif sortType=="WordTrigram":
    flist=filesplit.splitDataByWordNGrams(messageList,3)
elif sortType=="CharWordBigram":
    flist=filesplit.splitDataByWordCharNGrams(messageList,2,2)
elif sortType=="CharTrigramWordUnigram":
	flist=filesplit.splitDataByWordCharNGrams(messageList,1,3)
elif sortType=="Char4gramWordUnigram":
	flist=filesplit.splitDataByWordCharNGrams(messageList,1,4)
elif sortType=="CharBigramWordUnigram":
	flist=filesplit.splitDataByWordCharNGrams(messageList,1,2)
else:
    flist=[];
#Create the files necessary for training and testing
filesplit.toFiles(flist,messageList)
