import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 tabHardest.py inputf outputf")
        return
    lines = open(sys.argv[1],'r').readlines()
    of = sys.argv[2]
    model_scores = {}
    for i,line in enumerate(lines):
        if line != '\n':
            fields = line.strip('\n').split('\t')
            model = fields[-1].strip('\n')
            verbs = [fields[2],fields[4],fields[6],fields[8],fields[10]]
            info = [fields[13]] + verbs+fields[17:22]+[fields[-3],fields[-2],fields[-1]]
            pre = fields[14]
            targ = fields[15]
            post = fields[16]
            if post == '':
                #print("empty post")
                post = '.'
            key = '\t'.join([pre,targ,post]).replace('[SEP]','').replace('  ',' ').replace('  ',' ').strip()
            if key in model_scores:
                model_scores[key] += [info]
            else:
                model_scores[key] = [info]
    items = []
    ks = sorted(model_scores.keys())
    for i,k in enumerate(ks):
        if i > 0:
            neighbor = ks[i-1]
            if k[0:50] == neighbor[0:50] and k.split('\t')[1] == neighbor.split('\t')[1]:
                model_scores[k] += model_scores[neighbor]
                del model_scores[neighbor]
            elif k[0:25] == neighbor[0:25] and k.split('\t')[1] == neighbor.split('\t')[1]:
                neighbor_v = model_scores[neighbor]
                n_models = [e[-1] for e in neighbor_v]
                models = [e[-1] for e in model_scores[k]]
                overlap = [model for model in n_models if model in models]
                if len(overlap) == 0:
                    model_scores[k] += model_scores[neighbor]
                    del model_scores[neighbor]
            elif k[0:15] == neighbor[0:15] and k.split('\t')[1] == neighbor.split('\t')[1]:
                pass
                #print(k)
                #print(neighbor)

    for k,v in model_scores.items():
        models = [e[-1] for e in v]
        items.append([k,v,models,len(models)])
    highest = sorted(items,key=lambda i:-i[3])
    with open(of,'w') as outf:
        for h in highest:
            key = h[0]
            models = h[2]
            n_models = h[3]
            diffs = [float(e[-2]) for e in h[1]]
            info = h[1][0][0:-2]
            avg_diff = sum(diffs)/len(diffs)
            oline = '\t'.join([key]+info+[str(n_models),str(avg_diff),'_'.join(models)])
            outf.write(oline+'\n')
    
main()
