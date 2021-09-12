import sys

#Calculate and print average score on subset used for human judgments

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 get_human_accuracy.py results_file dataset")
        return
    results = [r.strip('\n').split('\t') for r in open(sys.argv[1],'r').readlines()]
    stems = [(r[3],r[15]) for r in results]
    come_go = [r[0] for r in stems if r[1]=='go' or r[1]=='come']
    manner = [r[0] for r in stems if r[1]!='go' and r[1]!='come']
    come_go_wins = [r for r in come_go if r=='True']
    manner_wins = [r for r in manner if r=='True']
    model = results[0][-1]
    dataset = sys.argv[2]
    total = float(len(results))
    come_go_total = float(len(come_go))
    manner_total = float(len(manner))
    wins = [r[3] for r in results if r[3]=='True']
    print('\t'.join([model,dataset,str(len(wins)),str(len(wins)/total),str(len(come_go_wins)),str(len(come_go_wins)/come_go_total),str(len(manner_wins)),str(len(manner_wins)/manner_total)]))
main()
