
for model in 'bert_base' \
       'bert_large' \
       'distil' \
       'gpt2_base' \
       'gpt2_large' \
       'gpt2_med' \
       'gpt2_xl' \
       'gpt' \
       'ngram_backward' \
       'ngram_forward' \
       'recurrent_ptb' \
       'recurrent_wiki' \
       'roberta' \
       'txl'

do
	python fix_comparison.py 'bert-syntax/results/'$model'_expt.tsv' > 'expt_results/'$model'_expt.tsv'
	python add_modeln.py 'expt_results/'$model'_expt.tsv' $model > 'expt_results/expt_results/'$model'_expt.tsv'
done

cat expt_results/expt_results/*_expt.tsv > expt_results_all.tsv
