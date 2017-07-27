#!/usr/bin/env bash

# see readme for the submodule: https://github.com/altosaar/fastText

RESULTDIR=/Users/jaanaltosaar/tmp/food2vec/fit/fasttext
DATADIR=/Users/jaanaltosaar/tmp/food2vec/dat/processed
echo $RESULTDIR

mkdir -p "${RESULTDIR}"

cd fastText
make
cd ..

NAME=all_recipes_train

./fastText/fasttext sentence_context -input $DATADIR/$NAME \
  -output "${RESULTDIR}"/model_$NAME -lr 0.025 -dim 100 \
  -ws 0 -epoch 1 -minCount 5 -neg 5 -loss hs -bucket 2000000 \
  -wordNgrams 0 \
  -minn 0 -maxn 0 -thread 8 -t 1 -lrUpdateRate 100 -saveOutput 1

tail -n+3 $RESULTDIR/model_$NAME.vec > $RESULTDIR/vectors_$NAME.txt

python ./fastText/eval_interactive.py -m "${RESULTDIR}"/vectors_$NAME.txt
