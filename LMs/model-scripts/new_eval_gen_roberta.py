# coding=utf-8
from transformers import BertForMaskedLM,BertTokenizer,RobertaForMaskedLM,RobertaTokenizer
import torch
import sys
import csv

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_names = {'roberta':'roberta-base'}
models = {'roberta':RobertaForMaskedLM}
tokenizers = {'roberta':RobertaTokenizer}

if len(sys.argv) < 4:
    print("Usage: python new_eval_gen_bert.py modelname data datatype",file=sys.stderr)

model_name = model_names[sys.argv[1]]
bert = models[sys.argv[1]].from_pretrained(model_name)
tokenizer = tokenizers[sys.argv[1]].from_pretrained(model_name)

print("using model:",model_name,file=sys.stderr)

only_prefix = False
if 'only_prefix' in sys.argv:
    only_prefix = True
    print("We take only the prefix", file=sys.stderr)

bert.eval()
bert.to(device)

def get_probs_for_words(sent,forms):
    pre,target,post=sent.split('***')
    if 'mask' in target.lower():
        target='<mask>'
    else:
        target=target
    sent = pre+target+post
    tokens = tokenizer.encode(sent, return_tensors="pt").to(device)
    mask_token_index = torch.where(tokens == tokenizer.mask_token_id)[1]
    #tokens=tokenizer.tokenize(pre)
    #target_idx=len(tokens)
    #print(target_idx)
    #tokens+=target
    #if not only_prefix:
    #    tokens+=tokenizer.tokenize(post)
    #tokens+=['[SEP]']
    #input_ids=tokenizer.convert_tokens_to_ids(tokens)
    #try:
    #    word_ids=tokenizer.convert_tokens_to_ids(forms)
    #except KeyError:
    #    print("skipping",forms[0],"bad wins")
    #    return None
    #tens=torch.LongTensor(input_ids).unsqueeze(0).to(device)
    word_ids = [tokenizer.convert_tokens_to_ids(tokenizer.tokenize(' '+f)) for f in forms]
    #print(word_ids, file=sys.stderr)
    with torch.no_grad():
        logits=bert(tokens)[0]
        mask_logits = logits[:,mask_token_index,:]
        res=torch.nn.functional.log_softmax(mask_logits,dim=-1)
    #print(res.size(),file=sys.stderr)
    scores = []
    for w in word_ids:
        #print(res[0,0,w],file=sys.stderr)
        score = res[0,0,w]
        #print(score,file=sys.stderr)
        scores.append(score)
    return [float(x.item()) for x in scores]

from collections import Counter

def eval_new():
    sflines = enumerate(open(sys.argv[2],encoding="utf8"))
    datatype = sys.argv[3]
    if datatype not in ['corpus','annotated','old']:
        print("Error: unrecognized input data type!",file=sys.stderr)
        return
    
    for i,line in sflines:
        #print(line,file=sys.stderr)
        if datatype != 'old':
            if datatype == 'corpus':
                pref,word,postf,subgenre,source,stem,genre,corpus,tense,gof,comef,drivef,walkf,arrivef = line.strip().split("\t")
            else: # 'annotated'
                pref,word,postf,subgenre,source,stem,genre,corpus,tense,embedding,subj,dest,notes,gof,comef,drivef,walkf,arrivef = line.strip().split('\t')
            masked = pref + " ***mask*** " + postf
            #masked = masked.replace('[SEP]','</s><s>') for some reason this doesn't help performance
            forms = [gof,comef,drivef,walkf,arrivef]
            pos = -1
            for i,f in enumerate(forms):
                if f == word:
                    pos = i
            if word not in forms:
                print("Error: form not identified correctly!",file=sys.stderr)
                pos = 0
        else: #Original data formatting
            na,_,masked,good,bad = line.strip().split('\t')
            forms = [good,bad]
            pos = 0
            word = None
        ps = get_probs_for_words(masked,forms)
        if ps is None:
            continue
        pairs = []
        for i,f in enumerate(forms):
            pairs.append(f)
            pairs.append(ps[i])
        #win = False
        #if ps[pos] == max(ps):
        #    win = True
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
        fields = [str(win),str(comego)]+pairs+[masked.encode("utf8")]
        if datatype != 'old':
            fields += [stem,pref,word,postf,corpus,genre,subgenre,source,tense]
        if datatype == 'annotated':
            fields += [embedding,subj,dest,notes]
        print(*fields,sep=u"\t")
        if i%100 == 0:
            print(i,file=sys.stderr)
            sys.stdout.flush()

eval_new()
