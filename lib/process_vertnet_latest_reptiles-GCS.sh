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
mv vertnet_latest_reptiles.csv.gz000000000006 rept6.csv.gz
mv vertnet_latest_reptiles.csv.gz000000000007 rept7.csv.gz
mv vertnet_latest_reptiles.csv.gz000000000008 rept8.csv.gz
mv vertnet_latest_reptiles.csv.gz000000000009 rept9.csv.gz
mv vertnet_latest_reptiles.csv.gz000000000010 rept10.csv.gz
mv vertnet_latest_reptiles.csv.gz000000000011 rept11.csv.gz
mv vertnet_latest_reptiles.csv.gz000000000012 rept12.csv.gz
mv vertnet_latest_reptiles.csv.gz000000000013 rept13.csv.gz
mv vertnet_latest_reptiles.csv.gz000000000014 rept14.csv.gz
mv vertnet_latest_reptiles.csv.gz000000000015 rept15.csv.gz
gunzip rept*
sed '1d' rept1.csv > tmp1
sed '1d' rept2.csv > tmp2
sed '1d' rept3.csv > tmp3
sed '1d' rept4.csv > tmp4
sed '1d' rept5.csv > tmp5
sed '1d' rept6.csv > tmp6
sed '1d' rept7.csv > tmp7
sed '1d' rept8.csv > tmp8
sed '1d' rept9.csv > tmp9
sed '1d' rept10.csv > tmp10
sed '1d' rept11.csv > tmp11
sed '1d' rept12.csv > tmp12
sed '1d' rept13.csv > tmp13
sed '1d' rept14.csv > tmp14
sed '1d' rept15.csv > tmp15
cat rept0.csv tmp1 tmp2 tmp3 tmp4 tmp5 tmp6 tmp7 tmp8 tmp9 tmp10 tmp11 tmp12 tmp13 tmp14 tmp15 > vertnet_latest_reptiles.csv
gzip vertnet_latest_reptiles.csv
gsutil cp vertnet_latest_reptiles.csv.gz gs://vertnet-byclass/vertnet_latest_reptiles.csv.gz
