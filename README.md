# Overview

This repository contains the data and code for ProSPer: Probing Human and Neural Network Language Model Understanding of Spatial Perspective, which appeared at BlackboxNLP (2021).

If you reuse this code or dataset, please cite it as:

Masis, Tessa and Carolyn Jane Anderson. ProSPer: Probing Human and Neural Network Language
Model Understanding of Spatial Perspective. Proceedings of the BlackboxNLP workshop at the Conference
on Empirical Methods in Natural Language Processing 2021.

There is also an associated Open Science Foundation repository (https://osf.io/qfz38/), which contains files related to the human experiments reported in the paper. You can find the task preregistration, experiment implementation code, human results, and analysis scripts there.

***

# Data

ProSPer's data set consists of two parts: the Annotated subset, which carries human annotations, and the Automatic subset, which is referred to as 'corpus' in this directory and README. The raw data for each subset can be found in annotated_data and corpus_data respectively.

Formatted versions of each file can be found in annotated_data/formatted and annotated_data/bert_format, and corpus_data/formatted and corpus_data/bert_format. (BERT requires slightly different data preparation than the other models because of differences in tokenization and masking.)

The compiled and formatted files for each subset can be found in the formatted and bert-formatted repositories. The Automatic subset is large enough that it has been split into 5 parts. The Annotated subset is small enough to run as one file.

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

cd into the LMs directory.

Run a BERT model on the annotated dataset:

```
python3 model-scripts/new_eval_gen_bert.py bert ../bert-formatted-files/bert_format_annotated_all.tsv annotated > results/bert_base_annotated.tsv
```

Pipe the results into an appropriately named file in bert-syntax/results, as above.

The first command-line argument specifies the type of BERT model:

* bert : base bert
* bert-large : large bert
* distil : distilBERT

## RUNNING GPT

cd into the LMs directory.

Run a GPT model on the annotated dataset:

```
python3 model-scripts/new_eval_gen_gpt.py gpt ../formatted-files/annotated_all.tsv annotated > results/got_base_annotated.tsv
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
python3 model-scripts/new_eval_gen_gpt.py gpt2 ../formatted-files/corpus_1.tsv corpus > results/gpt2_base_corpus/gpt2_base_corpus_1.tsv
```

The results files in the results/gpt2_base_corpus directory can then be cat-ed together into a full results file.

## RUNNING RoBERTa, Transformer-XL and CTRL

Other models are run similarly using scripts in LMs/model-scripts.

***

# Data Formatting

## Transformer format

To format a new corpus, your data should be in one of the following two formats:

### CORPUS STYLE:

sentence	subgenre	sourcefile

Additionally, you must supply the lemma, corpus, and genre.

If your data is in this format, you can format it for the transformer models by running formatfile.py (in the formatting directory) as below:

```
python3 formatting/formatfile.py "corpus_data/OANC_spoken_all/spoken_"$lemma"_all.txt" OANC_spoken $lemma "corpus_data/formatted/OANC_spoken_"$lemma".tsv"
```

### ANNOTATED STYLE:

prefix	lemma	postfix	embedding	persective/subject	destination	notes	genre	sourcefile

Additionally, you must supply the corpus and stem.


## RNNLM format

The RNNLM models take a different format. The recurrent_formatting.py script (in the formatting directory) can be used to create an RNNLM-formatted version of Transformer-formatted file as follows:

```
python3 recurrent_formatting.py input.tsv datatype rnn_model
```

There are two kinds of RNNLM models: one trained on the PTB corpus and one trained on the Wiki2 corpus. The data for these models must be formatted separately, because they have different vocabularies.

As an example, here is how to format the annotated data for the wiki model:

```
python3 formatting/recurrent_formatting.py annotated_all.tsv annotated wiki
```

The output is written to recurrent/data/annotated/wiki/test.txt.

In order to evaluate the results of RNNLM models using the Transformer evaluation scripts, you will need to format the results again using the recurrent_reformatting.py script (in the formatting directory) as shown below:

```
python3 formatting/recurrent_reformatting.py recurrent/results/annotated_wiki_word_discourse_rescore.txt annotated_all.tsv annotated > bert-syntax/results/recurrent_wiki_annotated.tsv
```

As shown above, pipe the output to a tsv file in the bert-syntax/results directory.

# Evaluation

LMs/eval_ext_stats.py is an evaluation script that runs on the format output by the transformer and n-gram models.

You can run this script on any LMs/results/.tsv file as follows:

```
python LMs/eval_ext_stats.py bert-syntax/results/ngram_corpus.tsv corpus
```

The second argument specifies whether the input data is in corpus or annotated format (i.e., does it contain annotations for embedding, subj/perspective-holder, destination?)

This script calculates 3 kinds of accuracy: overall accuracy in the 5-way prediction task; accuracy in the 2-way come/go task; and accuracy in the 2-way non-perspectival motion verb task.

It also prints accuracy breakdowns by corpus, embedding type, perspective-holder, and tense.

To get the scores rather than summary statistics, you may prefer to run getAllScores.py, which returns results ranked by model performance on each item.

Note: some models output log probabilities, others probabilities. You may need to use the scripts in LMs/score-conversion to convert to log format (which is expected by getAllScores.py).

# Human data

The items included in the human experiments can be found in human_judgments. The experimental data collected in the human experiments can be found in the associated Open Science Foundation repository (https://osf.io/qfz38/), along with the task preregistration, implementation code, and analysis scripts.
