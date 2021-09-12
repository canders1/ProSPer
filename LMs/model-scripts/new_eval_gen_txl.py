# coding=utf-8
from transformers import TransfoXLLMHeadModel, TransfoXLTokenizer
import torch
import sys
import csv

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if len(sys.argv) < 4:
    print("Usage: python new_eval_gen_bert.py modelname data datatype",file=sys.stderr)

model_name = 'transfo-xl-wt103'
model = TransfoXLLMHeadModel.from_pretrained(model_name)
tokenizer = TransfoXLTokenizer.from_pretrained(model_name)

print("using model:",model_name,file=sys.stderr)

only_prefix = False
if 'only_prefix' in sys.argv:
    only_prefix = True
    print("We take only the prefix", file=sys.stderr)

model.eval()
model.to(device)

def get_probs_for_words(sent,forms):
    toks = tokenizer.encode(sent, add_space_before_punct_symbol=True) #, add_special_tokens=True)
    input_ids = torch.tensor(toks).unsqueeze(0).to(device)  # Batch size 1
    in_tens = tokenizer(sent, return_tensors="pt",add_space_before_punct_symbol=True).to(device)
    outputs = model(**in_tens)
    prediction_scores, mems = outputs[:2]
    recent_preds = prediction_scores[0,-1,:]
    recent_preds = torch.nn.functional.log_softmax(recent_preds,-1)
    tok_forms = [tokenizer.encode(w, add_special_tokens=False) for w in forms]
    print([tokenizer.decode(t) for t in tok_forms],file=sys.stderr)
    form_preds = [float(recent_preds[i]) for i in tok_forms]
    return(form_preds)
   
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
            masked = pref
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
        pref_eos = pref.replace('<n>','<eos>')
        ps = get_probs_for_words(pref_eos,forms)
        if ps is None:
            continue
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
