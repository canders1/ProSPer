import sys

def main():
	if len(sys.argv) < 6:
		print("Usage: python3 data_to_items.py infile datatype start_idx nlists outfile")
		return
	inf = sys.argv[1]
	datatype = sys.argv[2]
	start_idx = int(sys.argv[3])
	nlists = int(sys.argv[4])
	outf = sys.argv[5]
	lines = open(inf,'r').readlines()
	len_lists = int(len(lines)/nlists)
	pref = "[[\""
	if datatype == "annotated":
		pref += "ann-"
	elif datatype == "corpus":
		pref += "scr-"
	nlines = []
	stem_counters = {"come":0,"go":0,"walk":0,"arrive":0,"drive":0}
	comes = []
	goes = []
	drives = []
	walks = []
	arrives = []
	for i,l in enumerate(lines):
		line = l.strip('\n').replace("\"","''").split('\t')
		stem = line[5]
		if stem == 'come':
			alt2 = line[13]
			alt1 = line[14]
			comes.append([line[0],alt1,alt2,line[2],i])
		elif stem == 'go':
			alt1 = line[13]
			alt2 = line[14]
			goes.append([line[0],alt1,alt2,line[2],i])
		elif stem == 'drive':
			alt1 = line[15]
			alt2 = line[16]
			drives.append([line[0],alt1,alt2,line[2],i])
		elif stem == 'walk':
			alt2 = line[15]
			alt1 = line[16]
			walks.append([line[0],alt1,alt2,line[2],i])
		elif stem == 'arrive':
			alt2 = line[14]
			alt1 = line[17]
			arrives.append([line[0],alt1,alt2,line[2],i])
		else:
			print("ERRROR!")
			print(l)
			print(stem)
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