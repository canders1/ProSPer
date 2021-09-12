n=47383;

for data in 'annotated' \
	 'corpus_all'
do
for model in 'bert_base' \
       'bert_large' \
       'distilbert' \
       'gpt2_base' \
       'gpt2_large' \
       'gpt2_med' \
       'gpt2_xl' \
       'gpt' \
       'roberta' \
       'txl'

do
	python3 getAllScores.py 'results/'$model'_'$data'.tsv' 'log' > 'new_all_scores/'$model'_'$data'.tsv'
	python3 ../add_modeln.py 'new_all_scores/'$model'_'$data'.tsv' $model > 'new_all_scores/add_names/'$model'_'$data'.tsv'
done

cat new_all_scores/add_names/*_$data'.tsv' > new_all_scores/$data'_scores_nonbaselines.tsv' 
done
