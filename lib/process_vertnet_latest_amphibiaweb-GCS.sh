#!/usr/bin/bash
rm tmp*
rm amph*.csv
rm vertnet_latest_amphibiaweb*
gsutil cp gs://vertnet-byclass/vertnet_latest_amphibiaweb* .
mv vertnet_latest_amphibiaweb.csv.gz000000000000 amphweb0.csv.gz
mv vertnet_latest_amphibiaweb.csv.gz000000000001 amphweb1.csv.gz
mv vertnet_latest_amphibiaweb.csv.gz000000000002 amphweb2.csv.gz
gunzip amphweb*
sed '1d' amphweb1.csv > tmp1
sed '1d' amphweb2.csv > tmp2
cat amphweb0.csv tmp1 tmp2 > vertnet_latest_amphibiaweb.csv
gzip vertnet_latest_amphibiaweb.csv
gsutil cp vertnet_latest_amphibiaweb.csv.gz gs://vertnet-byclass/vertnet_latest_amphibiaweb.csv.gz
