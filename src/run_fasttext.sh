#!/usr/bin/env bash

# run fasttext on data to generate food embeddings
# fasttext is a lightly modified version, described at https://github.com/altosaar/fastText

DATA=../dat/processed/all_recipes_train

NOW="$(date +'%Y-%m-%d')"
RESULTDIR=../fit/$NOW
echo $RESULTDIR

mkdir -p "${RESULTDIR}"

cd fastText
make
cd ..

./fastText/fasttext sentence_context -input $DATA \
  -output "${RESULTDIR}"/model -lr 0.025 -dim 100 \
  -ws 0 -epoch 1 -minCount 5 -neg 5 -loss hs -bucket 2000000 \
  -wordNgrams 0 \
  -minn 0 -maxn 0 -thread 8 -t 1 -lrUpdateRate 100 -saveOutput 1

tail -n+3 $RESULTDIR/model.vec > $RESULTDIR/vectors.txt

python ./fastText/eval_interactive.py -m "${RESULTDIR}"/vectors.txt
# usage: commands include nearest('beef'), nearest('banana') for example

