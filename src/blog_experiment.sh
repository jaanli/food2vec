#!/bin/bash

# create the training set
./process_kaggle_nature.sh

# get the sentence_word2vec module and compile the custom ops
git submodule update --init
cd sentence_word2vec
git submodule update --init
./compile_ops.sh

# run word2vec with the recipes as context
cd sentence_word2vec
python word2vec_optimized.py \
  --train_data ../../dat/processed/kaggle_and_nature_train \
  --interactive \
  --save_path /tmp \
  --subsample 0 \
  --eval 0 \
  --embedding_size 100
