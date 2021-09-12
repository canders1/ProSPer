"""
Script for outputting evaluation stats
"""
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python eval_ext_stats.py results.tsv datatype model")
        return
    datatype = sys.argv[2]
    lines = [l.split('\t') for l in open(sys.argv[1],'r').readlines()]
    total_wins = []
    comego_wins = []
    manner_wins = []
    go_scores = []
    come_scores = []
    drive_scores = []
    walk_scores = []
    arrive_scores = []
    masks = []
    stems = []
    prefixes = []
    words = []
    postfixes = []
    corpora = []
    genres = []
    subgenres = []
    sources = []
    tenses = []
    embeds = []
    subjs = []
    dests = []
    notes = []

    for i,l in enumerate(lines):
        l[3] = float(l[3])
        l[5] = float(l[5])
        l[7] = float(l[7])
        l[9] = float(l[9])
        l[11] = float(l[11])
        #total_wins.append(l[0])
        if l[13] == 'come':
            total_wins.append(str(l[5] > l[3] and l[5] > l[7] and l[5] > l[9] and l[5] > l[11]))
            comego_wins.append((i,l[1]))
        elif l[13] == 'go':
            total_wins.append(str(l[3] > l[5] and l[3] > l[7] and l[3] > l[9] and l[3] > l[11]))
            comego_wins.append((i,l[1]))
        elif l[13] == 'drive':
            total_wins.append(str(l[7] > l[3] and l[7] > l[5] and l[7] > l[9] and l[7] > l[11]))
            manner_wins.append((i,l[1]))
        elif l[13] == 'walk':
            total_wins.append(str(l[9] > l[3] and l[9] > l[5] and l[9] > l[7] and l[9] > l[11]))
            manner_wins.append((i,l[1]))
        elif l[13] == 'arrive':
            total_wins.append(str(l[11] > l[3] and l[11] > l[5] and l[11] > l[7] and l[11] > l[9]))
            manner_wins.append((i,l[1]))
        else:
            print("ERROR: unrecognized stem")
        go_scores.append(l[3])
        come_scores.append(l[5])
        drive_scores.append(l[7])
        walk_scores.append(l[9])
        arrive_scores.append(l[11])
        masks.append(l[12])
        stems.append(l[13])
        prefixes.append(l[14])
        words.append(l[15])
        postfixes.append(l[16])
        corpora.append(l[17])
        genres.append(l[18])
        subgenres.append(l[19])
        sources.append(l[20])
        tenses.append(l[21])
        if datatype == 'annotated':
            embeds.append(l[22])
            subjs.append(l[23])
            dests.append(l[24])
            notes.append(l[25])

    sep = "******************************************************"
    print(float(len(total_wins))) 
    total = float(len(total_wins))
    corr = float(len([i for i in total_wins if i=='True']))
    print("Total correct: "+str(corr))
    print("Total: "+str(total))
    print("Percentage correct: "+str(corr/total))
    
    print(sep)

    comego_total = float(len([i for i in comego_wins if i[1] != 'None']))
    comego_corr = float(len([i for i in comego_wins if i[1]=='True']))
    print("Come/go comparisons correct: "+str(comego_corr))
    print("Total come/go comparisons: "+str(comego_total))
    print("Percentage come/go comparisons correct: "+str(comego_corr/comego_total))

    manner_total = float(len([i for i in manner_wins if i[1] != 'None']))
    manner_corr = float(len([i for i in manner_wins if i[1]=='True']))
    print("Mannor of motion comparisons correct: "+str(manner_corr))
    print("Total manner of motion comparisons: "+str(manner_total))
    print("Percentage manner of motion comparisons correct: "+str(manner_corr/manner_total))
    
    print(sep)
    eval_subset(corpora,"Corpus",total_wins,comego_wins,manner_wins,stems)
    print(sep)
    eval_subset(tenses,"Tense",total_wins,comego_wins,manner_wins,stems)
    print(sep)

    '''
    context = [0 - 25, 26 - 50, 51 - 75, 76 - 100, 101+]
    '''
    pre_context = []
    for prefix in prefixes:
        if len(prefix.split()) < 26:        pre_context.append('0-25')
        elif len(prefix.split()) < 51:      pre_context.append('26-50')
        elif len(prefix.split()) < 76:      pre_context.append('51-75')
        elif len(prefix.split()) < 101:     pre_context.append('76-100')
        else:                               pre_context.append('101+')
    eval_subset(pre_context, "Prefix context", total_wins, comego_wins, manner_wins, stems)
    print(sep)
    post_context = []
    for postfix in postfixes:
        if len(postfix.split()) < 26:       post_context.append('0-25')
        elif len(postfix.split()) < 51:     post_context.append('26-50')
        elif len(postfix.split()) < 76:     post_context.append('51-75')
        elif len(postfix.split()) < 101:    post_context.append('76-100')
        else:                               post_context.append('101+')
    eval_subset(post_context, "Postfix context", total_wins, comego_wins, manner_wins, stems)
    print(sep)
    context = []
    for i in range(len(pre_context)):
        x = len(prefixes[i].split()) + len(postfixes[i].split())
        if x < 26:           context.append('0-25')
        elif x < 51:         context.append('26-50')
        elif x < 76:         context.append('51-75')
        elif x < 101:         context.append('76-100')
        else:                 context.append('101+')
    eval_subset(context, "Total context", total_wins, comego_wins, manner_wins, stems)
    print(sep)

    if datatype == 'annotated':
        eval_subset(embeds,'Embedding type',total_wins,comego_wins,manner_wins,stems,10,True)
        print(sep)
        eval_subset(subjs,'Subj/perspective holder',total_wins,comego_wins,manner_wins,stems,20,True)
        print(sep)

def eval_subset(field,label,wins,cg_wins,m_wins,stems,threshold=1,sepcomego=False):
    f_list = list(set(field))
    for f in f_list:
        f_sub = [(i,wins[i]) for i in range(len(wins)) if field[i]==f]
        f_total = float(len(f_sub))
        f_corr = float(len([w for w in f_sub if w[1]=='True']))
        f_idx = [i[0] for i in f_sub]
        f_comego = [comego[1] for comego in cg_wins if comego[0] in f_idx]
        f_comego_total = float(len(f_comego))
        f_comego_corr = float(len([w for w in f_comego if w=='True']))
        
        if f_total > threshold:
            print("")
            print(label+': '+f)
            print(label+' size: '+str(len(f_sub)))
            print("Total percentage correct: "+str(f_corr/f_total))
            if f_comego_total > 0:
                if sepcomego:
                    f_come = [come[1] for come in cg_wins if come[0] in f_idx and stems[come[0]]=='come']
                    f_go = [go[1] for go in cg_wins if go[0] in f_idx and stems[go[0]]=='go']
                    f_come_total = float(len(f_come))
                    f_go_total = float(len(f_go))
                    f_come_corr = float(len([w for w in f_come if w=='True']))
                    f_go_corr = float(len([w for w in f_go if w=='True']))
                    if f_come_total > 0.25*threshold:
                        print("Percentage come correct: "+str(f_come_corr/f_come_total))
                    if f_go_total > 0.25*threshold:
                        print("Percentage go correct: "+str(f_go_corr/f_go_total))
                else:
                    print("Percentage come/go correct: "+str(f_comego_corr/f_comego_total))
            else:
                print("Cannot calculate total percentage (zero instances)")
    return

main()
