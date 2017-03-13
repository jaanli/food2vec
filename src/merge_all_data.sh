#!/bin/bash

DIR=processed
# concatenate all datasets
touch $DIR/all_recipes.csv
cat $DIR/*.csv >> $DIR/all_recipes.csv

# print only second field onward
awk -F, '{print substr($0, index($0, $2))}' > $DIR/tmp.1

# convert commas to spaces
awk -F, '{$1=$1}1' OFS=" " tmp.1 > tmp.2

# keep recipes with at least two ingredients
awk -F" " 'NF>1' tmp.2 > $DIR/recipes_train

rm $DIR/tmp.*
