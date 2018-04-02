"""************************************************************************
PROJECT ENTITY RESOLUTION USING MACHINE LEARNING
	filesplit.py

This script aims to
1) Convert list of messages to a feature vector format
2) Output the files needed for training and testing for use by Sorter.py

************************************************************************"""
import os
import tokenizer
import re
basepath=os.path.dirname(os.path.abspath(__file__))
FREQUENCY_THRESHOLD = 100
def splitDataBySpace(messageList):
    featureList={}
    pureMsg = clearAuth(messageList)
    for message in pureMsg:
        listz = message.split()
        for token in listz:
            if token in featureList.keys():
                featureList[token]+=1
            else:
                featureList[token]=1
    featureFreqWrite(featureList)
    featureList = convertToWordVector(deleteLowFreq(featureList))
    writeToFile(featureList)
    return featureList

def splitDataByNGrams(messageList,n):
    featureList={}
    pureMsg = clearAuth(messageList)
    for message in pureMsg:
        listz = tokenizer.toNGrams(message,n)
        for token in listz:
            if token in featureList.keys():
                featureList[token]+=1
            else:
                featureList[token]=1
    featureFreqWrite(featureList)
    featureList = convertToWordVector(deleteLowFreq(featureList))
    writeToFile(featureList)
    return featureList

def splitDataByWordNGrams(messageList,n):
    featureList={}
    pureMsg = clearAuth(messageList)
    for message in pureMsg:
        listz = tokenizer.toWordNGrams(message,n)
        for token in listz:
            if token in featureList.keys():
                featureList[token]+=1
            else:
                featureList[token]=1
    featureFreqWrite(featureList)
    featureList = convertToWordVector(deleteLowFreq(featureList))
    writeToFile(featureList)
    return featureList

def splitDataByWordCharNGrams(messageList,wordn,charn):
    featureList={}
    pureMsg = clearAuth(messageList)
    for message in pureMsg:
        listz = tokenizer.toWordCharNGrams(message,wordn,charn)
        for token in listz:
            if token in featureList.keys():
                featureList[token]+=1
            else:
                featureList[token]=1
    featureFreqWrite(featureList)
    featureList = convertToWordVector(deleteLowFreq(featureList))
    writeToFile(featureList)
    return featureList
    

def writeToFile(featureList):
    featureFile = open(basepath+'/autogen/features.txt','w',encoding='UTF-8')
#write features to list
    for token,num in sorted(featureList.items(),key=lambda x:x[1]):
        featureFile.write("{} {}\n".format(token,num))
    featureFile.close()

def featureFreqWrite(featureList):
    featureFile = open(basepath+'/autogen/featureFreq.txt','w',encoding='UTF-8')
#write feature frequency to list
    for token,freq in sorted(featureList.items(),key=lambda x:x[1]):
        featureFile.write("{} {}\n".format(token,freq))
    featureFile.close()

def deleteLowFreq(featureList):
#remove features which have a low occuring frequency of <50
    copy = dict(featureList)
    for token,freq in copy.items():
        if freq < FREQUENCY_THRESHOLD:
            del featureList[token]
    return featureList

def convertToWordVector(featureList):
#Convert feature list into a feature:feature number vector
    counter = 1
    for token in featureList.keys():
        featureList[token]=counter
        counter+=1
    return featureList
    
def clearAuth(messageList):
#Remove the starting author number and space
    import re
    list2 = []
    for msg in messageList:
        msg=re.sub(r'^[0-9]+ ','',msg)
        list2.append(msg)
    return list2

def toFiles(featureList,messageList):
#Generate train.txt and test.txt files
    trainFile = open(basepath+'/autogen/train.txt','w',encoding='UTF-8')
    testFile = open(basepath+'/autogen/test.txt','w',encoding='UTF-8')
    messages = []
    authFreq={}
    authProcessed={}
#Convert message from raw text to a authornumber feature:feature number feature:feature number ........ list for each feature present
    for msg in messageList:
        newMessage=""
        auth=re.findall(r'^([0-9]+) ',msg)[0]
        newMessage+=auth
        if auth not in authFreq.keys():
            authFreq[auth]=1
        else:
            authFreq[auth]+=1
        msg=re.sub(r'^[0-9]+ ','',msg)
        for feature in featureList.keys():
            if feature in msg:
                newMessage+=" "+str(featureList[feature])+":1"
        newMessage+="\n"
        messages.append(newMessage)
#    trainfeatures={}
#    testfeatures={}
#Output to test or train files respectively in ratio of 3:7
    for msg in messages:
        auth=re.findall(r'^[0-9]+',msg)[0]
        if auth in authProcessed.keys():
            authProcessed[auth]+=1
        else:
            authProcessed[auth]=1
        if authProcessed[auth] < authFreq[auth]*3//10:
#            if auth in testfeatures.keys():
#                testfeatures[auth]+=re.findall(r'^[0-9]+ ?(.*)',msg)[0]+" "
#            else:
#                testfeatures[auth]=re.findall(r'^[0-9]+ ?(.*)',msg)[0]+" "
            testFile.write(msg)
        else:
#            if auth in trainfeatures.keys():
#                trainfeatures[auth]+=re.findall(r'^[0-9]+ ?(.*)',msg)[0]+" "
#            else:
#                trainfeatures[auth]=re.findall(r'^[0-9]+ ?(.*)',msg)[0]+" "
            trainFile.write(msg)
            
#Author by author classification
    """for key,item in sorted(trainfeatures.items(),key=lambda x:int(x[0])):
        newlist = sorted(list(set(item.split())),key=lambda x:int(x[:-2]))
        trainFile.write(key + " " + " ".join(newlist)+"\n")
    for key,item in sorted(testfeatures.items(),key=lambda x:int(x[0])):
        newlist = sorted(list(set(item.split())),key=lambda x:int(x[:-2]))
        testFile.write(key + " " + " ".join(newlist)+"\n")"""
    trainFile.close()
    testFile.close()
    print("done")
