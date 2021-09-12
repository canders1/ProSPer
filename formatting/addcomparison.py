"""
Script for adding inflected forms of verbs to compare
"""

import sys

def main():
    if len(sys.argv) < 5:
        print("Usage: python addcomparison.py inputf datatype verblist outputf")
        return()
    lines = [l.strip('\n').split('\t') for l in open(sys.argv[1],'r').readlines()]
    datatype = sys.argv[2]
    cats = [l.strip('\n').split('\t') for l in open(sys.argv[3],'r').readlines()]
    with open(sys.argv[4],'w') as of:
        for l in lines:
            if datatype == 'corpus':
                cat = int(l[-1])
            else:
                cat = int(l[8])
            if cat == -1:
                verbs = cats[0] #Fix this when -1 error is fixed
            else:
                verbs = cats[cat-1]
            if l[0] == '':
                l[0] = '**mask**'
            of.write('\t'.join(l+verbs)+'\n')
    return()
    
main()

