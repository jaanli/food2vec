#!/bin/bash

# Download test.json.zip and train.json.zip
# from https://www.kaggle.com/c/whats-cooking/data
# Put these in ../dat/

DIR=../dat
jq -s '.' $DIR/train.json $DIR/test.json > $DIR/kaggle.json
