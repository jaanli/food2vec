#!/bin/bash

# convert kaggle data to text

cat ../dat/test.json | jq -r '.[] | .ingredients  | @csv ' > tmp.1
cat ../dat/train.json | jq -r '.[] | .ingredients  | @csv ' > tmp.2
cat tmp.1 tmp.2 > ../dat/csv/kaggle.csv
