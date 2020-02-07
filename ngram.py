# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:44:32 2020

@author: Peter
@class : CMSC416 Natural Language Processing
@assignment : 2
@due date : 02/13/2020
@code : 129/202 lines
@MAIN METHOD : Starts on line 90

    Example run : ngram.py n m input-file/s
        --> n = N in N-gram = argv[1] so if N=2, then for words X Y Z, we consider X,Y the bigrams
        --> m = number of generated sentences  = argv[2]
        
"""
from sys import argv
import re
import numpy as np

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

''' A method to convert the integer count values of ngrams to percents of their wholes'''
def convert(n, nMinus):
    for prewords in n:
        total = nMinus[prewords]
        for thing2 in n[prewords]:
            n[prewords][thing2] = (n[prewords][thing2] / total) 
    return n
 
''' A method to get the current N-1 gram to analyze for next word addition'''
def N_Tokens(string,N):
    N = N-1 # I have no idea why this is going up by one, but decrement.
    tokens = tokenize(string)
    # Get the values from position (end - N) to the end. So for 8 words, N=3, it's only 7 and 8 (starting from 1)
    tokens = tokens[len(tokens)-N:len(tokens)] 
    # Turn them back into a string. Maybe make this a method
    toReturn = ""
    for _ in tokens:
        toReturn = toReturn + str(_) + " "
    return toReturn[:-1]

''' A method simply to parse the output strings, clean them up for readability. '''
def formatted(string):
    string = re.sub('(\s*<)|(>\s*)', '', string)
    string = re.sub(' \?', '?', string)
    string = re.sub(' !', '!', string)
    string = re.sub(' \.', '.', string)
    string = re.sub(' ,' , ',', string)
    string = re.sub('\b(hes)\b', 'he\'s', string)
    string = re.sub('\b(hers)\b', 'her\'s', string)
    string = re.sub('\b(cant)\b', 'can\'t', string)
    string = re.sub('\b(dont)\b', 'don\'t', string)
    string = re.sub('\b(theyre)\b', 'they\'re', string)
    string = re.sub('\b(youre)\b', 'you\'re', string)
    string = re.sub('\b(isnt)\b', 'isn\'t', string)
    string = re.sub('\b(havent)\b', 'haven\'t', string)
    string = re.sub('\bi\b', ' I ', string) # Why does nothing I do get this to work
    string = re.sub('\b(weve)\b', 'we\'ve', string)
    return string.capitalize()

'''-------------------------------------------------------------------------'''
'''---------------------------------MAIN------------------------------------'''
'''-------------------------------------------------------------------------'''

'''Handle command line arguments'''
n = int(argv[1]) # LETS ASSUME THREE FIRST? FOR TESTING
m = int(argv[2])
docs = getDocumentList()

'''Preprocessing done here'''
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
        # Combines this sentence @ x with the one after it, which is sentence x's punctuation
        string = toAdd[x] + " " + toAdd[(x+1)] 
        #Insert N-1 Starting Cursors, dubbed "<>" , and spacing, in front of sentence beginnings
        for N in range(1,n):
            string = precursor + string
        allSentences.append(string)
        x+=2 # skip by 2 (sentence + punctuation)+
    
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

''' For a single sentence in a dictionary of tokenized sentences'''
for A in tokenizedSentences:
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

''' Generate a new storage (maybe unneeded) of the words plus their respective weights'''
ngramsByPercent = convert(ngrams, nMinusOneGrams)
''' Generate the "start string" bit for all potential starts, robust to catch all values'''
startBrackets = ""
for number in range(0,n-1):
    startBrackets = startBrackets + '<> '
startBrackets = startBrackets[:-1] # Trim that last space
sentenceStarts = ngramsByPercent[str(startBrackets)] #str unneeded probably

''' Create 1D lists of pairwise values for each word and it's probability'''
probs = list(sentenceStarts.values())
words = list(sentenceStarts.keys())

    
outputSentences = []
sentencesToGo = m
while sentencesToGo > 0:
    ''' np.random.choice is critical. words and probs must be equal, 1D, and match perfectly, and sum to 1(probs)'''
    start = np.random.choice(words,1,p=probs) # Get the start of the sentence!
    forming = startBrackets +" "+ start[0] # choice always returns a set, so set[0] for 1 item
    currentNGram = N_Tokens(forming,n) # current N-1 gram to look up next words with
    
    ''' While no sentence end has been identified (by specified regex)'''
    while(re.search(r'([!|?|.])', forming) is None):
        forming = forming + " " # Add space on condition that not end of sentence
        ''' In double dictionary, get dictionary where first key is the currentNGram'''
        specifiedDictionary = ngramsByPercent[str(currentNGram)] 
        # From this specified dictionary, create a 1D list of it's keys and it's values 1:1 matching
        newProbs = list(specifiedDictionary.values())
        newWords = list(specifiedDictionary.keys())
        
        addition = np.random.choice(newWords,1,p=newProbs) # Word to be added
        forming = forming + addition[0]
        
        currentNGram = N_Tokens(forming,n) # Word has been added. Get next N-1Gram
    ''' Outside the while loop should be when the while loop identified an end punctuation'''    
    outputSentences.append(forming)
    sentencesToGo-=1 # Decrement number of sentences left to make


''' Outputting the sentences here'''
counter = 1
print("\n\n\n")
for _ in outputSentences:
    print("<<SENTENCE " +str(counter)+">>")
    print(formatted(_)+"\n")
    counter+=1
