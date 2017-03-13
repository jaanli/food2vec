#!/bin/bash

wget http://www.nature.com/article-assets/npg/srep/2011/111215/srep00196/extref/srep00196-s3.zip
unzip srep00196-s3.zip

tail -n+5 srep00196-s3.csv > processed/nature_data.csv

rm srep00196-s3.*

