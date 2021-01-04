#!/bin/bash

# convert scraped data to csv

IN=../dat/RecipesScraper/output
OUT=../dat/csv
for FILE in `find $IN -name '*.json'`
do
  NAME=`basename $FILE`
  jq -r '.recipes | .[] | .ingredients  | @csv ' $FILE > $OUT/$NAME.csv
done
