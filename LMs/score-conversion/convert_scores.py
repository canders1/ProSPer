
"""
Script for converting log probabilities to actual probabilities in results files
"""
import math
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_scores.py results.tsv")
        return
    lines = open(sys.argv[1],'r').readlines()
    rows = [l.strip('\n').split('\t') for l in lines]
    vdict = {1:3,2:5,3:7,4:9,5:11}
    ldict = {'go':3,'went':3,'gone':3,'goes':3,'going':3,
            'come':5,'came':5,'comes':5,'coming':5,
            'drive':7,'drove':7,'driven':7,'drives':7,'driving':7,
            'walk':9,'walked':9,'walks':9,'walking':9,
            'arrive':11,'arrived':11,'arrives':11,'arriving':11}
    newrows = []
    for r in rows:
        for i in [3,5,7,9,11]:
            r[i] = math.exp(float(r[i]))
        lemma = r[13]
        lscore = r[ldict[lemma]]
        if lscore != max([r[3],r[5],r[7],r[9],r[11]]):
            r[0] = False
        else:
            r[0] = True
        if ldict[lemma] == 3:
            r[1] = r[3] > r[5]
        elif ldict[lemma] == 5:
            r[1] = r[5] > r[3]
        elif ldict[lemma] == 7:
            r[1] = r[7] > r[9]
        elif ldict[lemma] == 9:
            r[1] = r[9] > r[7]
        elif ldict[lemma] == 11:
            r[1] = r[11] > r[5]
        else:
            print("Error: unrecognized stem")
        newrows.append([str(e) for e in r])
    for r in newrows:
        print('\t'.join(r))       

main()

