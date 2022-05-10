#import all the necessary libraries
import nltk
from nltk.corpus import stopwords
import pandas as pd
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
import string
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import mysql.connector as ml

#function to count the number of syllables in each word
def countSyllables(word):
    vowels = "aeiouy"
    numVowels = 0
    lastVowel = False
    for wc in word:
        foundVowel = False
        for v in vowels:
            if v == wc:
                if not lastVowel:
                    numVowels+=1   
                    foundVowel = lastWasVowel = True
                    break
        if not foundVowel:  
            lastVowel = False
    if len(word) > 2 and word[-2:] == "es":
        #Remove es 
        numVowels-=1
    elif len(word) > 1 and word[-1:] == "e":
        #remove silent e
        numVowels-=1
    return numVowels

#function to remove punctuations
def remove_punc(words):
    pfiltered_word=[]
    s=set(string.punctuation)
    for i in words:
            if i not in s:
                pfiltered_word.append(i)
    return pfiltered_word

#function to remove stop words
def remove_stop(pfiltered_word):
    wordsFiltered=[]
    stops = set(stopwords.words('english'))
    for w in pfiltered_word:
            if w not in stops:
                wordsFiltered.append(w)
    return wordsFiltered

#model prediction 
def model_pn(text1):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(text1)
    return sentiment_dict

#Find complex words from the filtered words
def compl_count(wordsFiltered):
    compl=[]
    for word in wordsFiltered:
            if countSyllables(word)>1:
                compl.append(word)
    return compl

#personal pronouns count
def count_pn(text):
    #list of personal pronouns 
    pn =["i","we","my","ours","us","our"]

    #tokenize the text to words without converting to lower case
    words=word_tokenize(text)

    #Now convert each word to lower case
    for word in words:
        #special care is taken for the word "US"
        if word != "US":
            word=word.lower

    #initialize personal pronouns count to zero
    pn_count=0

    #count number of personal pronouns
    for word in words:
        if word in pn:
            pn_count=pn_count+1
    return pn_count

#count number of words
def cnt_words(wordsFiltered):
    wlen=0
    for word in wordsFiltered:
        wlen=wlen+len(word)
    wlen=wlen/len(words)
    return wlen
                
for i in range(170):
    
    url_id=i+1
    url=str(url_id)+".txt"
    
    #this will open the txt file if exists
    try:
        #open the txt file if exist
        f=open(str(url_id)+".txt","r")

        #read data i.e. from the txt file
        text=f.read()

        #convert the whole text to lower case
        text1=text.lower()

        #tokenize the text to individual sentences
        sentences=sent_tokenize(text1)

        #tokenize the text to individual words
        words=word_tokenize(text1)
        words=remove_punc(words)

        #call remove_punc to remove punctuations from tokenized words           
        pfiltered_word= remove_punc(words)

        #now call remove_stop function to remove stop words from punctuation filtered words
        wordsFiltered=remove_stop( pfiltered_word)

        #sentiment analysis, function returns a dictionary
        sentiment_dict = model_pn(text1)

        #output 1
        positive=sentiment_dict['pos']

        #output2
        negative=sentiment_dict['neg']

        #output 3
        #polarity score
        Pol= (positive - negative )/ ((positive + negative) + 0.000001)

        #output 4
        #subjectivity score
        Subjective= (positive + negative)/ ((len(words)) + 0.000001)

        #output 9
        #count number of complex words in the text
        compl=compl_count(words)
        com=len(compl)

        #output 6
        #percentage of complex words in wordsFiltered(words without punctuation marks &stop words)
        Pcompl=100*(len(compl)/len(words))

        #output 5 &8
        #average sentence length        
        avgsenlen=len(words)/len(sentences)

        #output 7
        #compute FogIndex
        FI=0.4*(avgsenlen+Pcompl)

        #output 10
        count_w=len(wordsFiltered)

        #output 11
        syl_count=0
        for word in words:
            syl_count=syl_count+countSyllables(word)

        syl_count=syl_count/len(words)

        #output 12
        #count number of personal pronouns in the text
        pn_count=count_pn(text)

        #output 13
        #count average word length
        wlen=cnt_words(words)
        
        print(str(url_id)+"done")
            
        f.close()

        #now connect to mysql for updating the values in the table
        conc=ml.connect(host="localhost",user="root",passwd="9896",database="db")
        cur=conc.cursor()
        cur.execute("UPDATE inputs SET positive=%s,negative=%s,polarity=%s,subjectivity=%s,avgsenlen=%s,pcompl=%s,FI=%s,nmpsent=%s,compl=%s,wfilter=%s,syl_count=%s,pn_count=%s,avgwlen=%s WHERE url_id=%s",(positive,negative,Pol,Subjective,avgsenlen,Pcompl,FI,avgsenlen,com,count_w,syl_count,pn_count,wlen,url_id))
        frame = pd.read_sql("select * from inputs", conc)
        frame.to_excel("C:\Python\Blackcoffer\output.xlsx",index=False)
        conc.commit()
        cur.close()
        
    #if file doesn't exist the ide won't stop and won't show error
    except IOError:
        print(str(url_id)+"not acessible")
    
