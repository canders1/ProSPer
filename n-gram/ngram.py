import nltk.lm as lm
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE, KneserNeyInterpolated
from nltk.corpus import brown, reuters, gutenberg, treebank
import os
from nltk.tokenize import sent_tokenize, word_tokenize
import sys
from kneserngram import KneserNeyNGram
from math import log, exp

"""
Adapted from Giovanni Rescia. 2015. Procesamiento de lenguaje natural: https://github.com/giovannirescia/PLN-2015
"""

'''
Tri-gram 
Punctuation are tokens

Specify train corpus and n; turns a list of strings into a list of n-grams.
big_data is a list of Wikicorp files that are raw text data (strings)
'''

n = 3
dataset = sys.argv[1]
datatype = sys.argv[2]
mode = sys.argv[3]

def format_corp(corpus):
    text = []
    """
    for i,fn in enumerate(corpus):
        print("Processing file "+str(i)+" of "+str(len(corpus)))
        f = open(fn, 'rb')
        for line in f:
            '''skip first line and any empty lines'''
            line = line.decode(errors='ignore')
            if len(line) == 0 or line.isspace() or 'ENDOFARTICLE.' in line or line[0] == '<': 
                continue
            line = line.lower()
            sent = [word_tokenize(t) for t in sent_tokenize(line)]
            for each in sent:
                text.append(each)
        f.close()
    """

    text_and_brown = brown.sents()+reuters.sents()+gutenberg.sents()
    text = [s for s in text_and_brown]
    return text

### train forward ngram
text = format_corp(c)
'''
train, vocab = padded_everygram_pipeline(n, text)

lm = MLE(n)
lm.fit(train, vocab)
'''

'''train forward Kneser Ney ngram'''
lm2 = KneserNeyNGram(text,n,D=0.1)

'''train backward Kneser Ney ngram'''
text_b =[]
for each in text[::-1]:
    text_b.append(each[::-1])

lmb = KneserNeyNGram(text_b,n,D=0.1)

'''avg of the 2 ngrams'''
def for_back(verb, prefix, postfix):
    return (log(lm2.cond_prob(verb,tuple([x.decode('utf-8') for x in prefix])),2) + log(lmb.cond_prob(verb,tuple([x.decode('utf-8') for x in postfix])),2))/2

'''
input = [prefix, verb, postfix, subgenre, sourcefile, verb stems, supergenre, corpus]
input is tab-separated
output = [logprob of sentence, logprob of COME given prefix, logprob of GO given prefix, diff b/n COME and GO]
### Read in file, parse into list of input lists, and prints scores
'''
#inpfile = ""
#inp = open(inpfile,'r')

sflines = enumerate(open(dataset,encoding='utf8'))

for i,line in sflines:
    if datatype == 'corpus':
        pref,word,postf,subgenre,source,stem,genre,corpus,tense,gof,comef,drivef,walkf,arrivef = line.strip().split("\t")
    else: # 'annotated'
        pref,word,postf,subgenre,source,stem,genre,corpus,tense,embedding,subj,dest,notes,gof,comef,drivef,walkf,arrivef = line.strip().split('\t')
    forms = [gof,comef,drivef,walkf,arrivef]
    pos = -1
    for i,f in enumerate(forms):
        if f == word:
            pos = i
    if word not in forms:
        print("Error: form not identified correctly!",file=sys.stderr)
        pos = 0
    scores = []
    if mode == 'forward':
        prefix = word_tokenize(pref.lower())
        for f in forms:
            seq = prefix+[f]
            
            score = exp(lm2.sent_log_prob(seq))
            scores.append(score)
        #print(seq)
        #print(score)
    elif mode == 'backward':
        postfix = word_tokenize(postf.lower())
        for f in forms:
            seq = [f]+postfix[::-1]
            score = exp(lmb.sent_log_prob(seq))
            scores.append(score)
    else:
        print("Error: unrecognized mode!",file=sys.stderr)
    pairs = []
    for i,f in enumerate(forms):
        pairs.append(f)
        pairs.append(scores[i])
    if word == comef:
        comego = ps[1] > ps[0]
        win = ps[1] > ps[0] and ps[1] > ps[2] and ps[1] > ps[3] and ps[1] > ps[4]
    elif word == gof:
        comego = ps[0] > ps[1]
        win = ps[0] > ps[1] and ps[0] > ps[2] and ps[0] > ps[3] and ps[0] > ps[4]
    elif word == arrivef:
        comego = ps[4] > ps[1]
        win = ps[4] > ps[0] and ps[4] > ps[1] and ps[4] > ps[2] and ps[4] > ps[3]
    elif word == walkf:
        comego = ps[3] > ps[2]
        win = ps[3] > ps[0] and ps[3] > ps[1] and ps[3] > ps[2] and ps[3] > ps[4]
    elif word == drivef:
        comego = ps[2] > ps[3]
        win = ps[2] > ps[0] and ps[2] > ps[1] and ps[2] > ps[3] and ps[2] > ps[4]
    else:
        comego = None
    fields = [str(win),str(comego)]+pairs+[pref+word+postf]
    if datatype != 'old':
        fields += [stem,pref,word,postf,corpus,genre,subgenre,source,tense]
    if datatype == 'annotated':
        fields += [embedding,subj,dest,notes]
    print(*fields,sep=u"\t")
    
"""
for ex in inp:
    verb = ex[1].lower()
    prefix = word_tokenize(ex[0].lower())
    postfix = word_tokenize(ex[2].lower())[::-1]
    sent = word_tokenize(ex[0].lower() + verb + ex[2].lower())
    sentback = sent[::-1]

    sentprob = (lm2.sent_log_prob(sent) + lmb.sent_log_prob(sentback))/2.0
    come = for_back('come',prefix,postfix)
    go = for_back('go',prefix,postfix)
    diff = abs(come-go)

    #this part prints, so specify to where it should write in the command line
    print(str(sentprob) + '\t' + str(come) + '\t' + str(go) + '\t' + str(diff))

inp.close()
"""
'''
########################################################
### FOR TESTING PURPOSES
test_data = [[['He was','educated','at Eton and Christ church'],'genre','sourcefile','walk','supergenre','corpus']]

for each in test_data:
    verb = each[0][1]
    prefix = word_tokenize(each[0][0].lower())
    post = word_tokenize(each[0][2].lower())
    postfix = post[::-1]
    
    print('FORWARD NGRAM')
    print('logprob of VERB:')
    print(lm.logscore(verb))
    print('logprob of VERB given closest word in PREFIX:')
    print(lm.logscore(verb,[prefix[len(prefix)-1]]))
    print('logprob of VERB given PREFIX:')
    print(lm.logscore(verb,tuple(prefix)))

    come = lm.logscore('coming',tuple(prefix))
    go = lm.logscore('going',tuple(prefix))
    if come < go:
        print("Most likely word is COME: " + str(come))
    else:
        print("Most likely word is GO: " + str(go))
    print("Difference in likelihood is " + str(abs(come - go)))



    Input for Kneser-Ney is:
    1. Convert each word to unicode 
    2. Turn sequence of words into list
    3. Convert list into tuple
    
    print('\nKNESER NEY SMOOTHING')
    print('logprob of VERB:')
    print(log(lm2.cond_prob(verb),2))
    print('logprob of VERB given closest word in PREFIX:')
    print(log(lm2.cond_prob(verb, prev_tokens = tuple([prefix[len(prefix)-1].decode('utf-8')])),2))
    print('logprob of VERB given PREFIX:')
    print(log(lm2.cond_prob(verb, prev_tokens = tuple([x.decode('utf-8') for x in prefix])),2))
            
    come2 = log(lm2.cond_prob('coming', prev_tokens = tuple([x.decode('utf-8') for x in prefix])),2)
    go2 = log(lm2.cond_prob('going', prev_tokens = tuple([x.decode('utf-8') for x in prefix])),2)
    if come2 < go2:
       print('Most likely word is COME: ' + str(come2))
    else:
        print('Most likely word is GO: ' + str(go2))
    print('Difference in likelihood: ' + str(abs(come2 - go2)))

    
    print('\nBACKWARD NGRAM')
    print('logprob of VERB:')
    print(log(lmb.cond_prob(verb),2))
    print('logprob of VERB given closest word in POSTFIX:')
    print(log(lmb.cond_prob(verb,prev_tokens = tuple([postfix[len(postfix)-1].decode('utf-8')])),2))
    print('logprob of VERB given POSTFIX:')
    print(log(lmb.cond_prob(verb, prev_tokens = tuple([x.decode('utf-8') for x in postfix])),2))

    comeb = log(lmb.cond_prob('coming',prev_tokens=tuple([x.decode('utf-8') for x in postfix])),2)
    gob = log(lmb.cond_prob('going',prev_tokens = tuple([x.decode('utf-8') for x in postfix])),2)
    if comeb < gob:
        print('Most likely word is COME: ' + str(comeb))
    else:
        print('Most likely word is GO: ' + str(gob))
    print('Difference in likelihood is ' + str(abs(comeb - gob)))


    print('\nFORWARD-BACKWARD NGRAM')
    print('logprob of VERB:')
    print((log(lm2.cond_prob(verb),2)+log(lmb.cond_prob(verb),2))/2)
    print('logprob of VERB given PREFIX and POSTFIX:')
    print((log(lm2.cond_prob(verb,tuple([x.decode('utf-8') for x in prefix])),2)+log(lmb.cond_prob(verb,tuple([x.decode('utf-8') for x in postfix])),2))/2)
    
    comefb = (come2 + comeb)/2
    gofb = (go2 + gob)/2
    if comefb < gofb:
        print('Most likely word is COME: ' + str(comefb))
    else:
        print('Most likely word is GO: ' + str(gofb))
    print('Difference in likelihood is ' + str(abs(comefb - gofb)))
'''
