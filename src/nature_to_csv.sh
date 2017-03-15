#!/bin/bash

# convert nature data to csv

DIR=../dat

awk -F, '{print substr($0, index($0, $2))}' $DIR/processed/nature_data.csv > $DIR/csv/nature_data.csv
