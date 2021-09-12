for data in 'random' \
	 'hardest'
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
	python3 human_judgment_accuracy.py new_human_compare_results/$model'_'$data'.tsv' $data
done

done
