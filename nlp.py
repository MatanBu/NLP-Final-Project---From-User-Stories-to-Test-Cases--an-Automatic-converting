from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import spacy
from spacy import displacy
from scipy import spatial
from spacy.lang.en.stop_words import STOP_WORDS
from operator import itemgetter
from nlp_nltk import Porter_Stemmer
from textblob import TextBlob as tb
nlp = spacy.load('en')
import math
import itertools

def tf(word, blob):
        return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

def tokenize(str1):
    """ 
        Tokenize string input
    """
    doc = nlp(str1)
    tokens = []
    for token in doc:
        tokens.append((token.text,token.pos_))
        #print('"' + token.text +' -> ' + token.pos_ + '"')
    return tokens

def remove_stop_words(str1):
    """ 
        input: string
        output: string without stop words
    """
    str2=str1.lower()
    doc = nlp(str2)
    out = ""
    
    for word in doc:
        if word.is_stop == False:
            out+=str(word) + " "

    return out

def visualize(str1):
    doc = nlp(str1)
    #displacy.render(doc,style='dep')
    """ 
    svg = displacy.serve(doc, style = 'dep')
    """
    options = {'compact': True, 'bg': '#09a3d5',
           'color': 'white', 'font': 'Source Sans Pro'}
    html = displacy.render(doc, style='dep', options=options)
    
    #with open('vis1.svg','w',encoding='utf-8') as f:
    #    f.write(html)
    
    return html

def get_cosine_sim(str1,str2):
   
    doc1 = nlp(str1)
    doc2 = nlp(str2)
    return doc1.similarity(doc2)

def get_jaccard_sim(str1, str2): 
    
    s1 = Porter_Stemmer(str1)
    s2 = Porter_Stemmer(str2)
    a = set(s1.split()) 
    b = set(s2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

def find_cosine(sentencs,TCs):
    
    us = sentencs
    results = []
    for tc in TCs:
        sent = tc[1]
        disc = tc[0] + " " + tc[1]
        results.append((disc,get_cosine_sim(us, sent)))
    results.sort(key=takeSecond, reverse=True)
    return results

def find_jeccard(sentencs,TCs):
    
    us = sentencs
    results = []
    for tc in TCs:
        sent = tc[1] 
        disc = tc[0] + " " + tc[1]
        results.append((disc,get_jaccard_sim(us,sent)))
    results.sort(key=takeSecond, reverse=True)
    return results

def get_cosine_sim2(*strs): 
    vectors = [t for t in get_vectors(*strs)]
    return cosine_similarity(vectors)[0][1]
    
def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()

def find_cosine2(sentencs,TCs):
    
    us = sentencs
    results = []
    for tc in TCs:
        sent = tc[1] 
        disc = tc[0] + " " + tc[1]
        results.append((disc,get_cosine_sim2(us, sent)))
    results.sort(key=takeSecond, reverse=True)
    return results
        
def takeSecond(elem):
    return elem[1]    

def find_tfidf_match(tb_text,data):
    numOfTopRes=8
    tb_text=tb_text
    blob=tb(tb_text) #text formated for TextBlob
    US_TopWords=[] 
    TC_TopWords=[]
    wordsMatch=0 #num of US-TC matching words
    wordsMatchingList=[] #list of US-TC matching words: list of tuples (#TC,#wordsMatch))
    groupedWordsMatchingList=[] #list of US-TC matching words: list of tuples (#TC,#wordsMatch)) grouprd by TC's

    print("Top words in text:\n")
    scores = {word: tf(word, blob) for word in blob.words} #calculate TF for selected US
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True) #sorted list of results

    #add top words to US_TopWords list
    for word, score in sorted_words[:numOfTopRes]:
        US_TopWords.append(word)
        print("\t{} - TF: {}".format(word, round(score, 5)))

    blob=None #reset blob var
    bloblist =[]
    bloblist2 =[]

    #get TC's data into bloblist
    for tc in data:
        sent=tc[1]
        #disc=tc[0] + " " + tc[1]
        #TC_numbers.append((tc[0],))
        bloblist.append(sent)
    
    #format TC's text for TextBlob and put into bloblist2
    for tc in bloblist :
        bloblist2.append(tb(tc))

    #loop over TC's
    for i, blob2 in enumerate(bloblist2):
        print("Top words in TC {}".format(i + 1))
        scores2 = {word: tfidf(word, blob2 , bloblist2) for word in blob2.words} #calculate TF-IDF for each word in TC's
        sorted_words2 = sorted(scores2.items(), key=lambda x: x[1], reverse=True) #sorted list of results
        #add top words to TC_TopWords list
        for word, score in sorted_words2[:numOfTopRes]:
            TC_TopWords.append(tuple((i,word)))
            print("\t{}, TF-IDF: {}".format(word, round(score, 5)))

    #loop over TC_TopWords and US_TopWords to find matches words
    for i,TC in enumerate(TC_TopWords): 
        for word in US_TopWords:
            print("\n num: {},  TC NUM: {},  TC Word: {},  US word: {}".format(i, TC_TopWords[i][0], TC[1], word))
            if word==TC[1]:
                wordsMatch+=1
        wordsMatchingList.append(tuple((TC_TopWords[i][0],wordsMatch)))
        wordsMatch=0


    #group the matches of each TC together as a tuple: (TC num, # of matching words)
    g=itertools.groupby(wordsMatchingList, lambda x: x[0])
    for k,v in g:
        groupedWordsMatchingList.append((k, sum([x[1] for x in v])))

    print(groupedWordsMatchingList) #print for checking


    TC_num_desc_matches=[] #list to contain only TC that has matches words
    #loop over groupedWordsMatchingList and take only TC that have matches words
    #and put in list of tuples: (TC number, TC description, # of matching words
    for res in groupedWordsMatchingList:
        if res[1]>0:
            TC_num_desc_matches.append((data[res[0]][0],data[res[0]][1],res[1]))

    #sort list by # of matching words
    TC_num_desc_matches_sorted= sorted(TC_num_desc_matches, key=lambda x: x[2] ,reverse=True)

    out = []
    #print list 
    for tc in TC_num_desc_matches_sorted:
        out.append((tc[0]+" "+tc[1],tc[2]))
        print("\n{}".format(tc))

    return out


    
