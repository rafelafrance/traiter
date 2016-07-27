#!/usr/bin/bash
rm tmp*
rm rept*.csv
rm vertnet_latest_rept*
gsutil cp gs://vertnet-byclass/vertnet_latest_reptiles* .
mv vertnet_latest_reptiles.csv.gz000000000000 rept0.csv.gz
mv vertnet_latest_reptiles.csv.gz000000000001 rept1.csv.gz
mv vertnet_latest_reptiles.csv.gz000000000002 rept2.csv.gz
mv vertnet_latest_reptiles.csv.gz000000000003 rept3.csv.gz
mv vertnet_latest_reptiles.csv.gz000000000004 rept4.csv.gz
mv vertnet_latest_reptiles.csv.gz000000000005 rept5.csv.gz
gunzip rept*
sed '1d' rept1.csv > tmp1
sed '1d' rept2.csv > tmp2
sed '1d' rept3.csv > tmp3
sed '1d' rept4.csv > tmp4
sed '1d' rept5.csv > tmp5
cat rept0.csv tmp1 tmp2 tmp3 tmp4 tmp5 > vertnet_latest_reptiles.csv
gzip vertnet_latest_reptiles.csv
gsutil cp vertnet_latest_reptiles.csv.gz gs://vertnet-byclass/vertnet_latest_reptiles.csv.gz
