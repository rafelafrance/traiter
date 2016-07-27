#!/usr/bin/bash
rm tmp*
rm fish*.csv
rm vertnet_latest_fish*
gsutil cp gs://vertnet-byclass/vertnet_latest_fish* .
mv vertnet_latest_fishes.csv.gz000000000000 fish0.csv.gz
mv vertnet_latest_fishes.csv.gz000000000001 fish1.csv.gz
mv vertnet_latest_fishes.csv.gz000000000002 fish2.csv.gz
mv vertnet_latest_fishes.csv.gz000000000003 fish3.csv.gz
mv vertnet_latest_fishes.csv.gz000000000004 fish4.csv.gz
mv vertnet_latest_fishes.csv.gz000000000005 fish5.csv.gz
mv vertnet_latest_fishes.csv.gz000000000006 fish6.csv.gz
mv vertnet_latest_fishes.csv.gz000000000007 fish7.csv.gz
mv vertnet_latest_fishes.csv.gz000000000008 fish8.csv.gz
gunzip fish*
sed '1d' fish1.csv > tmp1
sed '1d' fish2.csv > tmp2
sed '1d' fish3.csv > tmp3
sed '1d' fish4.csv > tmp4
sed '1d' fish5.csv > tmp5
sed '1d' fish6.csv > tmp6
sed '1d' fish7.csv > tmp7
sed '1d' fish8.csv > tmp8
cat fish0.csv tmp1 tmp2 tmp3 tmp4 tmp5 tmp6 tmp7 tmp8 > vertnet_latest_fishes.csv
gzip vertnet_latest_fishes.csv
gsutil cp vertnet_latest_fishes.csv.gz gs://vertnet-byclass/vertnet_latest_fishes.csv.gz
