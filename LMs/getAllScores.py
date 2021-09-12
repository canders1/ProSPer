import sys
import math

'''
Takes a results file as first argument
Returns difference between scores for all examples, along with original data, in order of largest differences
'''


f = open(sys.argv[1], 'r').readlines()
scale = sys.argv[2]

top = []

for i,line in enumerate(f):
    parts = line.strip('\n').split('\t')+[str(i)]
    isFalse = parts[1].strip()
    isEx = parts[13].strip()
    stem = parts[15]
    come = float(parts[5].strip())
    go = float(parts[3].strip())
    drive = float(parts[7].strip())
    walk = float(parts[9].strip())
    arrive = float(parts[11].strip())
    if stem == parts[2]:
        alt2 = go
        alt1 = come
    elif stem == parts[4]:
        alt1 = go
        alt2 = come
    elif stem == parts[6]:
        alt1 = drive
        alt2 = walk
    elif stem == parts[8]:
        alt2 = drive
        alt1 = walk
    elif stem == parts[10]:
        alt2 = come
        alt1 = arrive
    else:
        pass
    if scale == 'log':
        log1 = math.exp(alt1)
        log2 = math.exp(alt2)
        top.append((abs(log1-log2),parts))
    else:
        top.append((abs(alt1-alt2),parts))

in_order = sorted(top,key=lambda x: -x[0])

for line in in_order:
    l = [str(f) for f in line[1]+[line[0]]]
    l_print = '\t'.join(l)
    print(l_print)
