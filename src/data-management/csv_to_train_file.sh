#!/bin/bash

# convert csv files to train file after removing stopwords

# merge all csv files
cat ../dat/csv/*.csv > tmp

# remove commas within text
tr ', ' ' ' <tmp >tmp.0
tr ' , ' ' ' <tmp.0 >tmp

# add delimeters
sed -i '' 's/" "/ XXX /g' tmp

# replace hyphens with underscores
tr '-' '_' <tmp >tmp.2

# remove non-alphabet characters, keep underscores
sed s'/[^A-Za-z_ ]/ /g' tmp.2 > tmp.3

# remove multiple spaces
tr -s ' ' <tmp.3 >tmp.2
mv tmp.2 tmp.3

# put commas back
sed 's/ XXX /, /g' tmp.3 > tmp.4

echo "total lines: `wc -l tmp.4`"

# lower case
tr '[:upper:]' '[:lower:]' <tmp.4 >tmp.5

# remove multiple spaces and underscores
tr -s '[:space:]' <tmp.5 >tmp.6
tr -s '_' <tmp.6 >tmp.7

# remove leading and trailing underscores
sed -i '' 's/ _/ /g' tmp.7
sed -i '' 's/_ / /g' tmp.7

# remove blacklist words
./remove.pl ../dat/blacklist.txt tmp.7 > tmp.0
echo "lines after removing blacklisted words: `wc -l tmp.0`"
tr -s ',[:space:]' <tmp.0 >tmp

# remove words longer than 30 chars
sed -i '' -e s'/[A-Za-z_]\{30,\}//g' tmp

# get word counts
tr -c '[:alnum:]' '[\n*]' < tmp | sort | uniq -c | sort -nr > word_counts
echo "word counts done"

# remove infrequent_words, those that appear less than 5 times
awk '($1 <= 5 ) ' word_counts > infrequent_word_counts
awk '{print $2} ' infrequent_word_counts > infrequent_words
echo "done making infrequent word list"
./remove.pl infrequent_words tmp > tmp.2
echo "lines after removing infrequent words: `wc -l tmp.2`"

# remove multiple commas
sed -i '' 's/, , /, /g' tmp.2
sed -i '' 's/, , /, /g' tmp.2
sed -i '' 's/, , /, /g' tmp.2

# remove spaces around commas
sed -i '' 's/ , /,/g' tmp.2
sed -i '' 's/, /,/g' tmp.2

# remove multiple spaces
tr -s ' ' <tmp.2 >tmp.3

# replace space with underscores
sed -i '' 's/ /_/g' tmp.3

# remove first and last char of each line
sed -i '' 's,.\(.*\).$,\1,g' tmp.3

# # replace commas with whitespace
tr ',' ' ' <tmp.3 >tmp.0

# keep recipes with at least two ingredients
awk -F" " 'NF>1' tmp.0 > ../dat/processed/train
echo "lines after removing single-ingredient recipes: `wc -l ../dat/processed/train`"

# rm tmp*
