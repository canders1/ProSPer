name=bert_format_corpus
head $name'_all.tsv' -n 10000 > $name'_1.tsv'
tail $name'_all.tsv' -n 37673 > corpus_tmp1
head corpus_tmp1 -n 10000 > $name'_2.tsv'
tail corpus_tmp1 -n 27673 > corpus_tmp2
head corpus_tmp2 -n 10000 > $name'_3.tsv'
tail corpus_tmp2 -n 17673 > corpus_tmp3
head corpus_tmp3 -n 10000 > $name'_4.tsv'
tail corpus_tmp3 -n 7673 > $name'_5.tsv'
rm corpus_tmp*

