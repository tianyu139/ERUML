"""************************************************************************
PROJECT ENTITY RESOLUTION USING MACHINE LEARNING
	tokenizer.py

This script aims to
1) Tokenize a message into its tokens(features)

************************************************************************"""
def toNGrams(message,n):
#To character ngrams
    newMessage=[]
    if len(message)-n+1>0:
        for i in range(len(message)-n+1):
           newMessage.append(message[i:i+n])
    return newMessage
def toWordCharNGrams(message,wordn,charn):
#To word character combination ngrams
    newMessage=toNGrams(message,charn)
    newMessage+=toWordNGrams(message,wordn)
    return newMessage
def smsTokenize(message):
#Split by space and emoticons
    import re
    import os
    f = open(os.path.dirname(os.path.abspath(__file__))+'/emoticons.txt')
    emoticons = []
    message=re.sub(r'([^-*OVov])([?.!]+)([^-*OVov])',r'\1 \2 \3',message)
#For all emoticons, add a space in front and behind it
    for emoticon in f:
        emoticon = emoticon.rstrip()
        message=re.sub(r'({})'.format(re.escape(emoticon)),r' \1 ',message)
    f.close()
    message=message.split()
    return message
def toWordNGrams(message,n):
#To word ngrams
    newMessage=[]
    message = smsTokenize(message)
    if len(message)-n+1>0:
        for i in range(len(message)-n+1):
            newMessage.append(" ".join(message[i:i+n]))
    return newMessage
