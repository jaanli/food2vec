#!/bin/bash

# append kaggle recipes to nature recipes
cp srep00196-s3.csv all-recipes.csv
cat kaggle_recipes.csv >> all-recipes.csv

# remove first four lines
tail -n+4 all-recipes.csv > recipes

# print only second field onward
gawk -iinplace -F, '{print substr($0, index($0, $2))}' recipes

# convert commas to spaces
gawk -iinplace -F, '{$1=$1}1' OFS=" " recipes

# keep recipes with at least two ingredients
gawk -iinplace -F" " 'NF>1' recipes


