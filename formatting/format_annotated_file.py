import sys
import re
import spacy
from pysbd.utils import PySBDFactory
'''
Applies to only one txt file at a time
Input and output are both TSV
'''

if len(sys.argv) < 6:
    print("Usage: python3 format_annotated_file.py fn corpus stem bert outputfn")

filename = sys.argv[1]
corpus = sys.argv[2]
stem = sys.argv[3]
bert = sys.argv[4]
outputfile = sys.argv[5]

f = open(filename,'r')
o = open(outputfile,'w')
nlp = spacy.blank('en')
nlp.add_pipe(PySBDFactory(nlp))

for line in f:
    parts = line.split('\t')
    prefix = parts[0].strip()
    lemma = parts[1].strip()
    postfix = parts[2].strip()
    embedding = parts[3].strip()
    subj = parts[4].strip()
    dest = parts[5].strip()
    notes = parts[6].strip()
    subgenre = parts[7].strip()
    sourcefile = parts[8].strip()

    if bert == 'bert':
        pref_sents = ' [SEP] '.join([str(i) for i in nlp(prefix).sents])
        post_sents = ' [SEP] '.join([str(i) for i in nlp(postfix).sents])
        prefix = pref_sents.replace('#','[SEP]').replace('[SEP] [SEP]','[SEP]')
        postfix = post_sents.replace('#','[SEP]').replace('[SEP] [SEP]','[SEP]')
    else:
        prefix = prefix.replace('#',' ').replace('  ',' ')
        postfix = postfix.replace('#',' ').replace('  ',' ')

    written = ['#blog#','#debate-transcript#','#email#','#essays#','#fiction#','#ficlets#','#government#','#govt-docs#','#jokes#','#journal#','#letters#','#movie-script#','#newspaper:newswire#','#non-fiction#','#spam#','#technical#','#travel_guides#','#travel-guides#','#twitter#']
    spoken = ['#telephone#','#face-to-face#','#court_transcript#','#debate_transcript#']
    if subgenre in written:
        supergenre = 'written'
    elif subgenre in spoken:
        supergenre = 'spoken'
    elif subgenre == 'natural':
        supergenre = 'natural'
    else:
        print("missing genre: "+subgenre)
        supergenre = subgenre
    
    cat1 = ['go','come','drive','walk','arrive']
    cat2 = ['going','coming','driving','walking','arriving']
    cat3 = ['went','came','drove','walked','arrived']
    cat4 = ['goes','comes','drives','walks','arrives']
    cat5 = ['gone','come','driven','walked','arrived']
    lemma = lemma.strip()
    if prefix[-2:] == 'to':
        tense = '1'
    elif lemma in cat2:
        tense = '2'
    elif lemma in cat3 and lemma not in cat5:
        tense = '3'
    elif lemma in cat5 and lemma not in cat3+cat1:
        tense = '5'
    elif lemma in cat1 and lemma not in cat5:
        tense = '1'
    elif lemma in cat4:
        tense = '4'
    else:
        if lemma != 'walked' and lemma != 'arrived' and lemma != 'come':
            print(lemma)
            print(text)
            print("Backing off")
        '''back-off thing where most previous word is checked for aux or modal, then next previous, up to 10 words'''
        noAux = True
        i = 1
        while noAux and i < 10:
            truncprefix = ' '.join(prefix.split()[-i:])
            if re.search("(had)|(have)|(has)|('d)|('ve)",truncprefix):
                noAux = False
                if lemma in cat5:
                    tense = '5'
            elif re.search("(might)|(may)|(must)|(would)|(do)|('ll)|(will)|(can)|(could)|(should)|(shall)|(won't)",truncprefix):
                noAux = False
                if lemma in cat1:
                    tense = '1'
            else:
                i += 1
        if noAux and lemma in cat3:
            tense = '3'
        elif noAux and lemma in cat1:
            tense = '1'
        elif noAux:
            tense = '-1'
            print(lemma)
            print(truncprefix)
    '''
    output = [prefix, verb, postfix, subgenre, sourcefile, verb stem, supergenre, corpus, tense/aspect]
    '''
    o.write('\t'.join([prefix, lemma, postfix, subgenre, sourcefile, stem, supergenre, corpus, tense, embedding, subj, dest, notes]))
    o.write('\n')

f.close()
o.close()

