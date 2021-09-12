"""
Script for outputting evaluation stats
"""
import sys

def main():

    lines = open(sys.argv[1],'r').readlines()
    scores = [l.split('\t')[0] for l in lines]
    total = float(len(scores))
    corr = float(len([i for i in scores if i=='True']))
    print("Total correct: "+str(corr))
    print("Total: "+str(total))
    print("Percentage correct: "+str(corr/total))
main()
