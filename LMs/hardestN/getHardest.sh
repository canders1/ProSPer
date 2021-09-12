n=1000;

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
	python3 findHardestEx.py '../results/'$model'_'$data'.tsv' $n 'log' > 'new_hardestN/'$n'/'$model'_'$data'_'$n'.tsv'
	python3 ../../formatting/add_modeln.py 'new_hardestN/'$n'/'$model'_'$data'_'$n'.tsv' $model > 'new_hardestN/'$n'/add_names/'$model'_'$data'.tsv'
done

for model in 'ngram_backward' \
       'ngram_forward' \
       'recurrent_ptb' \
       'recurrent_wiki' 
do
        python3 findHardestEx.py '../results/'$model'_'$data'.tsv' $n 'prob' > 'new_hardestN/'$n'/'$model'_'$data'_'$n'.tsv'
        python3 ../../formatting/add_modeln.py 'new_hardestN/'$n'/'$model'_'$data'_'$n'.tsv' $model > 'new_hardestN/'$n'/add_names_baseline/'$model'_'$data'.tsv'
done

cat new_hardestN/$n/add_names/*_$data'.tsv' > new_hardestN/$data'_hardest_'$n'_nonbaselines.tsv'
cat new_hardestN/$n/add_names_baseline/*_$data'.tsv' > new_hardestN/$data'_hardest_'$n'_baselines.tsv'
cat new_hardestN/$data'_hardest_'$n'_'*'baselines.tsv' > new_hardestN/$data'_hardest_'$n'_all.tsv' 
done
