import sys
import math

"""
File for reformatting the results of a recurrent model into the results scoring format used by the BERT/GPT models
"""

def main():
    if len(sys.argv) < 4:
        print("Usage: python recurrent_reformatting.py results origdata datatype")
        return

    results = [r.strip('\n').split('\t') for r in open(sys.argv[1],encoding='utf8').readlines()]
    origdata = open(sys.argv[2],encoding='utf8').readlines()
    datatype = sys.argv[3]
    curr_idx = 0
    for i,line in enumerate(origdata):
        if datatype == 'corpus':
            pref,word,postf,subgenre,source,stem,genre,corpus,tense,gof,comef,drivef,walkf,arrivef = line.strip().split("\t")
        else: # 'annotated'
            pref,word,postf,subgenre,source,stem,genre,corpus,tense,embedding,subj,dest,notes,gof,comef,drivef,walkf,arrivef = line.strip().split('\t')
        
        forms = [gof,comef,drivef,walkf,arrivef]
        curr_res = [r for r in results[curr_idx:curr_idx+5]]
        curr_forms = [r[1] for r in curr_res]
        if curr_forms != forms:
            print("Alignment error!",file=sys.stderr)
            print(forms,file=sys.stderr)
            print(curr_forms,file=sys.stderr)
        ps = [math.exp(float(p[0])) for p in curr_res]
        
        for i,f in enumerate(forms):
            if f == word:
                pos = i
        if word not in forms:
            print("Error: form not identified correctly!",file=sys.stderr)
            pos = 0
        pairs = []
        for i,f in enumerate(forms):
            pairs.append(f)
            pairs.append(ps[i])
        
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
        fields = [str(win),str(comego)]+pairs+[None]
        if datatype != 'old':
            fields += [stem,pref,word,postf,corpus,genre,subgenre,source,tense]
        if datatype == 'annotated':
            fields += [embedding,subj,dest,notes]
        print(*fields,sep=u"\t")
        curr_idx += 5

main()
