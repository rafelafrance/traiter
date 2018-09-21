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
mv vertnet_latest_fishes.csv.gz000000000009 fish9.csv.gz
mv vertnet_latest_fishes.csv.gz000000000010 fish10.csv.gz
mv vertnet_latest_fishes.csv.gz000000000011 fish11.csv.gz
mv vertnet_latest_fishes.csv.gz000000000012 fish12.csv.gz
mv vertnet_latest_fishes.csv.gz000000000013 fish13.csv.gz
mv vertnet_latest_fishes.csv.gz000000000014 fish14.csv.gz
mv vertnet_latest_fishes.csv.gz000000000015 fish15.csv.gz
mv vertnet_latest_fishes.csv.gz000000000016 fish16.csv.gz
mv vertnet_latest_fishes.csv.gz000000000017 fish17.csv.gz
mv vertnet_latest_fishes.csv.gz000000000018 fish18.csv.gz
mv vertnet_latest_fishes.csv.gz000000000019 fish19.csv.gz
mv vertnet_latest_fishes.csv.gz000000000020 fish20.csv.gz
gunzip fish*
sed '1d' fish1.csv > tmp1
sed '1d' fish2.csv > tmp2
sed '1d' fish3.csv > tmp3
sed '1d' fish4.csv > tmp4
sed '1d' fish5.csv > tmp5
sed '1d' fish6.csv > tmp6
sed '1d' fish7.csv > tmp7
sed '1d' fish8.csv > tmp8
sed '1d' fish9.csv > tmp9
sed '1d' fish10.csv > tmp10
sed '1d' fish11.csv > tmp11
sed '1d' fish12.csv > tmp12
sed '1d' fish13.csv > tmp13
sed '1d' fish14.csv > tmp14
sed '1d' fish15.csv > tmp15
sed '1d' fish16.csv > tmp16
sed '1d' fish17.csv > tmp17
sed '1d' fish18.csv > tmp18
sed '1d' fish19.csv > tmp19
sed '1d' fish20.csv > tmp20
cat fish0.csv tmp1 tmp2 tmp3 tmp4 tmp5 tmp6 tmp7 tmp8 tmp9 tmp10 tmp11 tmp12 tmp13 tmp14 tmp15 tmp16 tmp17 tmp18 tmp19 tmp20 > vertnet_latest_fishes.csv
gzip vertnet_latest_fishes.csv
gsutil cp vertnet_latest_fishes.csv.gz gs://vertnet-byclass/vertnet_latest_fishes.csv.gz
