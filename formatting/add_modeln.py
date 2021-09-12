import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python add_modeln.py inputf modeln")
        return
    lines = open(sys.argv[1],'r').readlines()
    lines_out = [l.strip('\n')+'\t'+sys.argv[2]+'\n' for l in lines]
    for l in lines_out:
        print(l)

main()
