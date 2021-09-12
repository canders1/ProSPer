cat lemmalist.txt | while read lemma 
do
	echo $lemma;
	python3 formatfile.py "../corpus_data/OANC_spoken_all/spoken_"$lemma"_all.txt" OANC_spoken $lemma gpt "../corpus_data/formatted/OANC_spoken_"$lemma".tsv";
	python3 formatfile.py "../corpus_data/OANC_written_all/written_1_"$lemma"_all.txt" OANC_written $lemma gpt "../corpus_data/formatted/OANC_written_1_"$lemma".tsv";
	python3 formatfile.py "../corpus_data/OANC_written_all/written_2_"$lemma"_all.txt" OANC_written $lemma gpt "../corpus_data/formatted/OANC_written_2_"$lemma".tsv";
	python3 formatfile.py "../corpus_data/masc_spoken_all/spoken_"$lemma"_all.txt" masc_spoken $lemma gpt "../corpus_data/formatted/masc_spoken_"$lemma".tsv";
	python3 formatfile.py "../corpus_data/masc_written_all/written_"$lemma"_all.txt" masc_written $lemma gpt "../corpus_data/formatted/masc_written_"$lemma".tsv";
done
cat '../corpus_data/formatted/'*'_'*'.tsv' > '../corpus_data/formatted/all.tsv'

python3 addcomparison.py ../corpus_data/formatted/all.tsv corpus ../categories.txt ../corpus_data/corpus_all.tsv

python3 format_annotated_file.py "../annotated_data/annotated_ex_arrive.tsv" natural arrive gpt "../annotated_data/formatted/formatted_annotated_arrive.tsv"
python3 format_annotated_file.py "../annotated_data/annotated_ex_come.tsv" natural come gpt "../annotated_data/formatted/formatted_annotated_come.tsv"
python3 format_annotated_file.py "../annotated_data/annotated_ex_drive.tsv" natural drive gpt "../annotated_data/formatted/formatted_annotated_drive.tsv"
python3 format_annotated_file.py "../annotated_data/annotated_ex_go.tsv" natural go gpt "../annotated_data/formatted/formatted_annotated_go.tsv"
python3 format_annotated_file.py "../annotated_data/annotated_ex_walk.tsv" natural walk gpt "../annotated_data/formatted/formatted_annotated_walk.tsv"
cat '../annotated_data/formatted/formatted_annotated_'*'.tsv' > '../annotated_data/formatted/all.tsv'

python3 addcomparison.py ../annotated_data/formatted/all.tsv annotated ../categories.txt ../annotated_data/annotated_all.tsv
