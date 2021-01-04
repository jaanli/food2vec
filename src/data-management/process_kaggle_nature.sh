#!/bin/bash

DIR=../dat

# remove first four lines
tail -n+4 $DIR/kaggle_and_nature.csv > recipes.1

# print only second field onward
awk -F, '{print substr($0, index($0, $2))}' recipes.1 > recipes.2

# convert commas to spaces
awk -F, '{$1=$1}1' OFS=" " recipes.2 > recipes.3

# keep recipes with at least two ingredients
awk -F" " 'NF>1' recipes.3 > recipes.4

cp recipes.4 $DIR/processed/kaggle_and_nature_train

rm recipes.*
