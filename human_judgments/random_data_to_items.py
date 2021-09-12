import sys
import random

def main():
	if len(sys.argv) < 6:
		print("Usage: python3 random_data_to_items.py infile start_idx nlists list_len outfile")
		return
	inf = sys.argv[1]
	start_idx = int(sys.argv[2])
	nlists = int(sys.argv[3])
	len_lists = int(sys.argv[4])
	outf = sys.argv[5]
	total_len = len_lists*nlists
	print(total_len)
	lines = open(inf,'r').readlines()
	pref = "[[\"random-"

	stem_counters = {"come":0,"go":0,"walk":0,"arrive":0,"drive":0}
	comes = []
	goes = []
	drives = []
	walks = []
	arrives = []

	randlines = [p for p in enumerate(lines)]
	random.shuffle(randlines)
	while (len(comes)+len(goes)+len(drives)+len(walks)+len(arrives)) < total_len:
		i,l = randlines.pop()
		prefix,target,postfix,stem,go,come,drive,walk,arrive,corpus,genre,subgenre,source,tense,n_models,avg_error,model_list = l.strip('\n').replace("\"","''").split('\t')
		#print(target)
		if target == come:
			alt2 = go
			alt1 = come
			comes.append([prefix,alt1,alt2,postfix,i,'come'])
		elif target == go:
			alt1 = go
			alt2 = come
			goes.append([prefix,alt1,alt2,postfix,i,'go'])
		elif target == drive:
			alt1 = drive
			alt2 = walk
			drives.append([prefix,alt1,alt2,postfix,i,'drive'])
		elif target == walk:
			alt2 = drive
			alt1 = walk
			walks.append([prefix,alt1,alt2,postfix,i,'walk'])
		elif target == arrive:
			alt2 = come
			alt1 = arrive
			arrives.append([prefix,alt1,alt2,postfix,i,'arrive'])
		else:
			print("ERRROR!")
			print(l)
			print(target)
	print(len(comes)+len(goes)+len(drives)+len(walks)+len(arrives))
	nlines = []
	for stem,stem_list in [("go",goes),("come",comes),("drive",drives),("walk",walks),("arrive",arrives)]:
		stem_idx = start_idx
		for i,line in enumerate(stem_list):
			latin_idx = stem_idx
			if (latin_idx-start_idx)+1 > len_lists:
				stem_idx = start_idx
				latin_idx = stem_idx
			lp = pref+stem+"-"+str(line[4])+"\","+str(latin_idx)+"], \"AcceptabilityJudgment\", {\"s\":"
			nl = ' '.join([lp,"\""+line[0],"_____",line[3]+"\",","\"as\": [\""+line[1]+"\",","\""+line[2]+"\"]}],\n"])
			nlines.append(nl)
			stem_idx += 1
	with open(outf,'w') as of:
		for l in nlines:
			of.write(l)
	return

main()