#!/bin/bash

DIR=../dat/processed

# merge all datasets
cat $DIR/*.csv >> $DIR/all_recipes.csv

# print only second field onward
awk -F, '{print substr($0, index($0, $2))}' $DIR/all_recipes.csv > $DIR/tmp.1

# convert commas to spaces
awk -F, '{$1=$1}1' OFS=" " $DIR/tmp.1 > $DIR/tmp.2

# keep recipes with at least two ingredients
awk -F" " 'NF>1' $DIR/tmp.2 > $DIR/recipes_train

rm $DIR/tmp.*
