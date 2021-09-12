from transformers import CTRLLMHeadModel, CTRLTokenizer
import math
import torch
import sys
import csv
import logging
import itertools
from collections import Counter


logging.basicConfig(level=logging.INFO)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if len(sys.argv) < 4:
    print("Usage: python new_eval_gen_ctrl.py data datatype genre", file=sys.stderr)

'''
Possible genres: Links, Books, Wikipedia, Reviews, Translation, News, multilingual, Questions, Explain, and then all the reddit ones
'''


model_name = "ctrl"
model = CTRLLMHeadModel.from_pretrained(model_name)
tokenizer = CTRLTokenizer.from_pretrained(model_name)
print("using model: {}".format(model_name), file=sys.stderr)

model.eval()
model.to(device)

def get_probs_for_words(sent,forms):
    pre, target, post = sent.split("***")
    if "mask" in target.lower():
        target = ["[MASK]"]
    else:
        target = tokenizer.tokenize(target)
    # Add genre label here
    pre = ' '.join(pre.split())
    tokens = tokenizer.tokenize(sys.argv[3]+" "+pre)
    target_idx = len(tokens)

    toks = []
    for i,w in enumerate(forms):
        t = tokenizer.tokenize(w)
        if len(t) > 1:
            print("Word split at index:"+str(i)+" , taking first seg", file=sys.stderr)
            t = t[0]
        toks.append(t)
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    wids = []
    for t in toks:
        wid = tokenizer.convert_tokens_to_ids(t)
        wids.append(wid)
    if len(input_ids) == 1:
        print("skipping",pre,forms[0],"empty beggingin")
        return None

    # Compute scores for w1 and w2
    add_tok_ws = []
    scores = []
    for i in wids:
        add_tok_ws.append([])
        scores.append(0)
    add_tok_w1 = []
    score_w1 = 0
    for i,ids_w in enumerate(wids):
        tens = torch.LongTensor([input_ids + add_tok_ws[i]]).to(device)
        with torch.no_grad():
            res = model(tens)[0]
            res = res[..., 0:model.config.vocab_size]
            res = torch.nn.functional.log_softmax(res, dim=-1)
        if ids_w is not None:
            scores[i] += res[0, -1, ids_w].item()
        add_tok_ws[i].append(ids_w if ids_w is not None else [0])

    return [math.exp(float(s)) for s in scores]


def eval_new():
    extended = False
    datatype = sys.argv[2]
    if datatype not in ['corpus','annotated','old']:
        print("Error: unrecognized input data type!",file=sys.stderr)
        return
    for i, line in enumerate(open(sys.argv[1], encoding="utf8")):
        if datatype != 'old':
            if datatype == 'corpus':
                pref, word, postf, subgenre, source, stem, genre, corpus, tense, gof, comef, drivef, walkf, arrivef = line.strip().split("\t")
            else: #annotated
                pref,word,postf,subgenre,source,stem,genre,corpus,tense,embedding,subj,dest,notes,gof,comef,drivef,walkf,arrivef = line.strip.split("\t")
            masked = pref + " ***mask*** " + postf
            forms = [gof, comef, drivef, walkf, arrivef]
            pos = -1
            for i,f in enumerate(forms):
                if f == word:
                    pos = i
            if word not in forms:
                print("Error: form not identified correctly!",file=sys.stderr)
                pos =0
        else: #original data formatting
            na, _, masked, good, bad = line.strip().split("\t")
            forms = [good,bad]
            pos = 0
            word = None
        ps = get_probs_for_words(masked,forms)
        if ps is None: continue
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
        if i % 100 == 0:
            print(i, file=sys.stderr)
            sys.stdout.flush()

eval_new()



