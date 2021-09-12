import sys
import re


'''
Applies to one tsv file at a time, output is a txt file of the same name
'''

if len(sys.argv) < 4:
    print("Usage: python recurrent_formatting.py input.tsv datatype rnnlm_model") 

filename = sys.argv[1]
#outputdest = "recurrent/data/"+sys.argv[2]+"/"
if sys.argv[3] == 'ptb':
    vocabfile = "recurrent/ptb_word_discourse_relative-path_tf1.4_gh/labels.tsv"
    outputdest = "recurrent/data/"+sys.argv[2]+"/ptb/"
elif sys.argv[3] == 'wiki':
    vocabfile = "recurrent/wiki2_word_discourse_relative-path_tf1.4_gh/labels.tsv"
    outputdest = "recurrent/data/"+sys.argv[2]+"/wiki/"
else:
    print("Error: unknown vocab type")

f = open(filename, 'r')

cats = [ ['go','come','drive','walk','arrive'],
        ['going','coming','driving','walking','arriving'],
        ['went','came','drove','walked','arrived'],
        ['goes','comes','drives','walks','arrives'],
        ['gone','come','driven','walked','arrived'] ]
newlines = []
vlist = []
for line in f:
    parts = line.split('\t')
    prefix = parts[0].strip().lower()
    tense = parts[8].strip()
    
    ''' Insert <eos> instead of periods '''
    #prefix = re.sub(r"(\. )|(\? )|(! )", r" <eos> ", prefix)
    ''' Separate all punctuation with white space'''
    prefix = re.sub(r"(\p)", r" \1 ", prefix)
    prefix = re.sub(r"\s{2,}", r" ", prefix)
    ''' Insert <unk> for OOV words '''
    sep_prefix = prefix.split()
    newprefix = []
    for word in sep_prefix:
        if word not in open(vocabfile).read():
            word = "<unk>"
        newprefix.append(word) 
    prefix = ' '.join(newprefix)

    newlines.append(prefix)
    vlist.append(cats[int(tense)-1])
with open(outputdest+'test.txt','w') as tf:
    for i,pref in enumerate(newlines):
        verbs = vlist[i]
        for verb in verbs:
            tf.write(pref + " " + verb + "<eos>\n")
            
f.close()
