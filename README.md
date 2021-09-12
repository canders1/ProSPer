# Overview

***

# Running Instructions

Instructions for running each kind of model are below. The n-gram, Transformer XL, BERT, and GPT models all take the same format as input. The RNNLM models require you to format the data differently--- directions on that can be found in the data formatting section of this README.

## RUNNING N-GRAM MODEL

cd into the n-gram directory.

ngram.py contains code for training and running both a forward and a backward n-gram model, trained on the NLTK Reuters, Brown, and Gutenberg corpora.

The models use Kneyser Ney smoothing.

To run a forward n-gram model on the annotated dataset, run:

```
python3 ngram.py ../annotated_all.tsv annotated forward > ../bert-syntax/results/ngram_annotated.tsv
```

Pipe the results into a tsv file as above.

## RUNNING RNNLM

cd into the recurrent directory. 

This is a clone of https://github.com/lverwimp/tf-lm (code for Verwimp, Lyan, Van hamme, Hugo and Patrick Wambacq. 2018. TF-LM: TensorFlow-based Language Modeling Toolkit. LREC 2018).

There are two pretrained models: one trained on the Penn TreeBank (ptb) and one trained on WikiText2 (wiki).

configs are found in the config directory--- these are divided into configs for the wiki model and configs for the ptb model. There are configs of each kind for the corpus and annotated datasets.

To run a wiki model on the annotated dataset, run:

```
python scripts/main.py --config config/wiki/annotated_en-wiki_word_discourse_rescore.config 
```

Results will appear in results/annotated_wiki_word_discourse_rescore.txt 

To run a ptb model on a subset of the corpus dataset, run:

```
python scripts/main.py --config config/wiki/corpus2_en-wiki_word_discourse_rescore.config 
```

You will need to use the recurrent_reformatting.py script to format the results into the style expected by the evaluation scripts in bert-syntax.

## RUNNING BERT

cd into the bert-syntax directory.

Run a BERT model on the annotated dataset:

```
python3 new_eval_gen_bert.py bert ../annotated_all.tsv annotated > results/bert_base_annotated.tsv
```

Pipe the results into an appropriately named file in bert-syntax/results, as above.

The first command-line argument specifies the type of BERT model:

* bert : base bert
* bert-large : large bert
* roberta : RoBERTa
* distil : distilBERT

## RUNNING GPT

cd into the bert-syntax directory.

Run a GPT model on the annotated dataset:

```
python3 new_eval_gen_gpt.py gpt ../annotated_all.tsv annotated > results/got_base_annotated.tsv
```

Pipe the results into an appropriately named file in bert-syntax/results, a
s above.

The first command-line argument specifies the type of GPT model:

* gpt : base gpt
* gpt2-med : medium GPT2
* gpt2-large : large GPT2
* gpt2-xl : XL GPT2

GPT is slow enough that it is best to run subsets of the corpus dataset. For instance:

```
python3 new_eval_gen_gpt.py gpt2 ../corpus_1.tsv corpus > results/gpt2_base_corpus/gpt2_base_corpus_1.tsv
```

The results files in the results/gpt2_base_corpus directory can then be cat-ed together into a full results file.

***

# Data Formatting

## Transformer format

To format a new corpus, your data should be in one of the following two formats:

### CORPUS STYLE:

sentence	subgenre	sourcefile

Additionally, you must supply the lemma, corpus, and genre.

If your data is in this format, you can format it for the transformer models by running formatfile.py as below:

```
python3 formatfile.py "scraped_data/OANC_spoken_all/spoken_"$lemma"_all.txt" OANC_spoken $lemma "scraped_data/formatted/OANC_spoken_"$lemma".tsv"
```

Pipe the output to a file as shown above.

### ANNOTATED STYLE:

prefix	lemma	postfix	embedding	persective/subject	destination	notes	genre	sourcefile

Additionally, you must supply the corpus and stem.



## RNNLM format

The RNNLM models take a different format. The recurrent_formatting.py script can be used to create an RNNLM-formatted version of Transformer-formatted file as follows:

```
python3 input.tsv datatype rnn_model
```

There are two kinds of RNNLM models: one trained on the PTB corpus and one trained on the Wiki2 corpus. The data for these models must be formatted separately, because they have different vocabularies.

As an example, here is how to format the annotated data for the wiki model:

```
python3 annotated_all.tsv annotated wiki
```

The output is written to recurrent/data/annotated/wiki/test.txt.

In order to evaluate the results of RNNLM models using the Transformer evaluation scripts, you will need to format the results again using the recurrent_reformatting.py script as shown below:

```
python3 recurrent_reformatting.py recurrent/results/annotated_wiki_word_discourse_rescore.txt annotated_all.tsv annotated > bert-syntax/results/recurrent_wiki_annotated.tsv
```

As shown above, pipe the output to a tsv file in the bert-syntax/results directory.

# Evaluation

bert-syntax/eval_ext_stats.py is an evaluation script that runs on the format output by the transformer and n-gram models.

You can run this script on any bert-syntax/results/.tsv file as follows:

```
python bert-syntax/eval_ext_stats.py bert-syntax/results/ngram_corpus.tsv corpus
```

The second argument specifies whether the input data is in corpus or annotated format (i.e., does it contain annotations for embedding, subj/perspective-holder, destination?)

This script calculates 3 kinds of accuracy: overall accuracy in the 5-way prediction task; accuracy in the 2-way come/go task; and accuracy in the 2-way non-perspectival motion verb task.

It also prints accuracy breakdowns by corpus, embedding type, perspective-holder, and tense.

# Human data

The items included in the human experiments can be found in human_judgments. The experimental data collected in the human experiments can be found in the associated Open Science Foundation repository (https://osf.io/qfz38/), along with the task preregistration, implementation code, and analysis scripts.
