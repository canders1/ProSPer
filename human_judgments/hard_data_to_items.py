import sys

def main():
	if len(sys.argv) < 5:
		print("Usage: python3 data_to_items.py infile start_idx nlists outfile")
		return
	inf = sys.argv[1]
	start_idx = int(sys.argv[2])
	nlists = int(sys.argv[3])
	outf = sys.argv[4]
	lines = open(inf,'r').readlines()
	len_lists = int(len(lines)/nlists)
	pref = "[[\"hard-"
	nlines = []
	stem_counters = {"come":0,"go":0,"walk":0,"arrive":0,"drive":0}
	items = []
	for i,l in enumerate(lines):
		prefix,target,postfix,stem,go,come,drive,walk,arrive,corpus,genre,subgenre,source,tense,n_models,avg_error,model_list = l.strip('\n').replace("\"","''").split('\t')
		if target == come:
			alt2 = go
			alt1 = come
			items.append([prefix,alt1,alt2,postfix,i,'come'])
		elif target == go:
			alt1 = go
			alt2 = come
			items.append([prefix,alt1,alt2,postfix,i,'go'])
		elif target == drive:
			alt1 = drive
			alt2 = walk
			items.append([prefix,alt1,alt2,postfix,i,'drive'])
		elif target == walk:
			alt2 = drive
			alt1 = walk
			items.append([prefix,alt1,alt2,postfix,i,'walk'])
		elif target == arrive:
			alt2 = come
			alt1 = arrive
			items.append([prefix,alt1,alt2,postfix,i,'arrive'])
		else:
			print("ERRROR!")
			print(l)
			print(target)
	latin_idx = start_idx
	for i,line in enumerate(items):
		stem = line[5]
		if (latin_idx-start_idx)+1 > len_lists:
			latin_idx = start_idx
		lp = pref+stem+"-"+str(line[4])+"\","+str(latin_idx)+"], \"AcceptabilityJudgment\", {\"s\":"
		nl = ' '.join([lp,"\""+line[0],"_____",line[3]+"\",","\"as\": [\""+line[1]+"\",","\""+line[2]+"\"]}],\n"])
		nlines.append(nl)
		latin_idx += 1
	with open(outf,'w') as of:
		for l in nlines:
			of.write(l)
	return

main()