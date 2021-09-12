import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_comparison.py inputf")
        return
    lines = open(sys.argv[1],'r').readlines()
    fields = [l.strip('\n').split('\t') for l in lines]
    for i,l in enumerate(fields):
        l[3] = float(l[3])
        l[5] = float(l[5])
        l[7] = float(l[7])
        l[9] = float(l[9])
        l[11] = float(l[11])
        if l[13] == 'come' or l[13] == 'came':
            l[0] = l[5] > l[3] and l[5] > l[7] and l[5] > l[9] and l[5] > l[11]
        elif l[13] == 'go':
            l[0] = l[3] > l[5] and l[3] > l[7] and l[3] > l[9] and l[3] > l[11]
        elif l[13] == 'drive':
            l[0] = l[7] > l[3] and l[7] > l[5] and l[7] > l[9] and l[7] > l[11]
        elif l[13] == 'walk':
            l[0] = l[9] > l[3] and l[9] > l[5] and l[9] > l[7] and l[9] > l[11]
        elif l[13] == 'arrive':
            l[0] = l[11] > l[3] and l[11] > l[5] and l[11] > l[7] and l[11] > l[9]
        else:
            print("ERROR: unrecognized stem")
            print(l[13])
        print('\t'.join([str(i) for i in l]))

main()
