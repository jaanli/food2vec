#!/bin/bash

# convert kaggle data to text
cat ../dat/test.json | jq -r '.[] | .ingredients  | @csv ' > tmp

# remove quotes
cat tmp | tr -d '"' > tmp.1

# lower case
tr '[:upper:]' '[:lower:]' <tmp.1 >tmp.2

# replace hyphens with underscores
tr '-' '_' <tmp.2 >tmp.4

# remove blacklist words
grep -i -F -w -v -f ../dat/blacklist.txt tmp.4 > tmp.5


tr -c '[:alnum:]' '[\n*]' < tmp.5 | sort | uniq -c | sort -nr > word_counts

# remove infrequent_words
awk '($1 <= 5 ) ' word_counts > infrequent_word_counts
awk '{print $2} ' infrequent_word_counts > infrequent_words
grep -i -F -w -v -f infrequent_words tmp.5 > tmp.6

# replace spaces with underscores
tr ' ' '_' <tmp.6 >tmp.7

# replace commas with whitespace
tr ',' ' ' <tmp.7 >final

rm tmp*
