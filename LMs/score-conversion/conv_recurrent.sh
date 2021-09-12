for f in results/recurrent*.tsv
do
   echo $f
   python3 convert_scores.py $f > results/conv_$f
done
