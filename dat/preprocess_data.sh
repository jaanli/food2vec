#!/bin/bash

# concatenate all datasets
touch all-recipes.csv
cat srep00196-s3.csv >> all-recipes.csv
cat kaggle_recipes.csv >> all-recipes.csv
cat allrecipes_recipes.csv >> all-recipes.csv
cat jamieoliver_recipes.csv >> all-recipes.csv

# remove first four lines
tail -n+4 all-recipes.csv > recipes.1

# print only second field onward
awk -F, '{print substr($0, index($0, $2))}' recipes.1 > recipes.2

# convert commas to spaces
awk -F, '{$1=$1}1' OFS=" " recipes.2 > recipes.3

# keep recipes with at least two ingredients
awk -F" " 'NF>1' recipes.3 > recipes.4

cp recipes.4 recipes


