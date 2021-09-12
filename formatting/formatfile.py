import sys
import re
import spacy
from pysbd.utils import PySBDFactory
'''
Applies to only one txt file at a time
Input and output are both TSV
'''

if len(sys.argv) < 6:
    print("Usage: python3 formatfile.py filename corpus lemma bert outputfile")

filename = sys.argv[1]
corpus = sys.argv[2]
lemma = sys.argv[3]
bert = sys.argv[4]
outputfile = sys.argv[5]
maxlength = 800

f = open(filename,encoding='utf8')
o = open(outputfile,'w')

nlp = spacy.blank('en')
nlp.add_pipe(PySBDFactory(nlp))

for line in f:
    parts = line.split('\t')
    text = parts[0].strip()
    subgenre = parts[1].strip()
    sourcefile = parts[2].strip()
    
    written = ['#blog#','#debate-transcript#','#email#','#essays#','#fiction#','#ficlets#','#government#','#govt-docs#','#jokes#','#journal#','#letters#','#movie-script#','#newspaper:newswire#','#non-fiction#','#spam#','#technical#','#travel_guides#','#travel-guides#','#twitter#']
    spoken = ['#telephone#','#face-to-face#','#court_transcript#','#debate_transcript#']
    if subgenre in written:
        supergenre = 'written'
    elif subgenre in spoken:
        supergenre = 'spoken'
    else:
        print("missing genre: "+subgenre)
    if lemma.startswith('c'):
        stem = 'come'
    elif lemma.startswith('g') or lemma.startswith('went'):
        stem = 'go'
    elif lemma.startswith('w'):
        stem = 'walk'
    elif lemma.startswith('a'):
        stem = 'arrive'
    elif lemma.startswith('d'):
        stem = 'drive'
    text = text.replace('<n>',' ')
    if bert=='bert':
        text_sents = ' [SEP] '.join([str(i) for i in nlp(text).sents])
        text_sep = text_sents.replace('#','[SEP]').replace('[SEP] [SEP]','[SEP]')
    else:
        text_sep = text.replace('#',' ').replace('  ',' ')
    text = text_sep.split(lemma)
    prefix = text[0].strip()
    if len(prefix) > maxlength:
        prefix = prefix[len(prefix)-maxlength:]
    postfix = text[1].strip()
    if len(postfix) > maxlength:
        postfix = postfix[0:maxlength+1]
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
    o.write('\t'.join([prefix, lemma, postfix, subgenre, sourcefile, stem, supergenre, corpus, tense])) 
    o.write('\n')

f.close()
o.close()

