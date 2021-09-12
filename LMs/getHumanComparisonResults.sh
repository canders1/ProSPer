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
	python3 ../human_judgments/idx_to_results.py ../human_judgments/$data'_result_line_ids.txt' new_all_scores/$model'_corpus_all.tsv' $model new_human_compare_results/$model'_'$data'.tsv'
done

done
