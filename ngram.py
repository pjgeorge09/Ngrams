# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:44:32 2020

@author: Peter
@class : CMSC416 Natural Language Processing
@assignment : 2
@due date :

    Example run : ngram.py n m input-file/s
        --> n = N in N-gram = argv[1] so if N=2, then for words X Y Z, we consider X,Y the bigrams
        --> m = number of generated sentences  = argv[2]
        
"""
from sys import argv
import re
import pandas as pd
import numpy as np
import random

''' Method to get a list of all the documents. Returns list of docs.'''
def getDocumentList():
    toReturn = [] # A list of docs from arguments
    for _ in range(len(argv) - 3):
        aDoc = str(argv[_ + 3])
        toReturn.append(aDoc)
    return toReturn

''' Method to remove the period after Mr. Mrs. Dr. Miss. Ms. Expected to be capitalized'''
def fixSomePeriods(document):
    document = re.sub('Mr.', 'Mr', document)
    document = re.sub('Mrs.', 'Mrs', document)
    document = re.sub('Ms.', 'Ms', document)
    document = re.sub('Dr.', 'Dr', document)
    document = re.sub('Miss.', 'Miss', document)
    document = re.sub('U.S.A.', 'USA', document)
    document = re.sub('U.S.' , 'US' , document)
    document = re.sub(',' , ' ,', document) # IMPORTANT: This line separates commas
    return document
    
''' Turn any string into an array of tokens based on white space(+)
    Regex tools used : re.split on white space'''
def tokenize(phrase):
    return re.split('\s+', phrase)

''' A method to parse each tokenized sentence and count unigrams'''
def getUnigrams(aTokenizedSentence):
    global unigrams
    for aToken in aTokenizedSentence:
        if aToken not in unigrams.keys():
            unigrams[aToken] = 1
        else:
            unigrams[aToken] += 1
    return

''' A method to convert the integer count values of ngrams to percents of their wholes'''
def convert(n, nMinus):
    for prewords in n:
        total = nMinus[prewords]
        for thing2 in n[prewords]:
            n[prewords][thing2] = (n[prewords][thing2] / total) 
    return n
    

'''---------------------------------MAIN------------------------------------'''
'''Handle command line arguments'''
n = int(argv[1]) # LETS ASSUME THREE FIRST?
m = int(argv[2])
docs = getDocumentList()

'''Preprocessing done here. TODO: Make a method'''
allSentences = []
for _ in docs:
    toAdd = []
    File = open(_,'r')
    toAdd = File.read()
    toAdd = fixSomePeriods(toAdd) # See method
    toAdd = re.sub('[\”|\“|\"|\’|\'|‘]', '', toAdd) # Destroy all quotes
    toAdd = re.sub('\)|\(', "" , toAdd) # Destroy all parenthesis
    toAdd = re.sub('\\n|\\ufeff', ' ', toAdd) # Destroy these weird tokens
    toAdd = re.split(r'([!|?|.])', toAdd)
    x = 0
    while x < len(toAdd)-1:
        precursor = "<> "
        string = toAdd[x] + " " + toAdd[(x+1)]
        for N in range(1,n):
            string = precursor + string
        allSentences.append(string)
        x+=2
    
''' Turn dictionary of strings into dictionary of dictionaries (nested dict being
    tokenized sentences to include their punctutation'''
tokenizedSentences = []    
for _ in allSentences:
    temp = tokenize(_)
    if len(temp) > (n + (n-1)):
        tokenizedSentences.append(temp)
        
''' Dictionaries everywhere! unigrams for special case when n=1'''        
ngrams = dict()
nMinusOneGrams = dict()
unigrams = dict()

''' For a single sentence in a dictionary of tokenized sentences'''
for A in tokenizedSentences:
    getUnigrams(A) # Unigram Case
    ''' For a token in a tokenized sentence'''
    for B in range(0,len(A)):
        ''' On the condition that it is not the added start symbols'''
        if A[B] != "<>":
            start = B #Word placement to start
            end = B-(n) #Word placement to end
            ''' xCol will be the words that come before the word analyzed'''
            xCol = ""
            ''' For every word from start to end, working backwards with start being analyzed word'''
            for C in A[end+1:start]:
                xCol =  xCol+" "+ C
            xCol = xCol[1:] #truncate the final space added by the last addition (Which is at the front)
            ''' If this phrase has never been seen before'''
            if xCol not in ngrams.keys():
                ngrams[xCol] = {} # Init ngrams with the phrase
                ngrams[xCol][(A[start])] = 1 # Set the phrase and analyzed word count to 1 for first occurance
                nMinusOneGrams[xCol] = 1 # Also record the phrase in the nMinus dict
            else:
                nMinusOneGrams[xCol] += 1
                ''' If this phrase has been seen before, but not for this analyzed word'''
                if A[start] not in ngrams[xCol]:
                    ngrams[xCol][A[start]] = 1
                else:
                    ngrams[xCol][A[start]] +=1

ngramsByPercent = ngrams
ngramsByPercent = convert(ngrams, nMinusOneGrams)
temp = ngramsByPercent['<> <>']
probs = list(temp.values())
words = list(temp.keys())
print(words)
print(sum(probs))
print(np.random.choice(words,1,p=probs))    



        
           
    

    


