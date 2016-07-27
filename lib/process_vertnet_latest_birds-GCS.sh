#!/usr/bin/bash
rm tmp*
rm bird*.csv
rm vertnet_latest_bird*
gsutil cp gs://vertnet-byclass/vertnet_latest_birds* .
mv vertnet_latest_birds.csv.gz000000000000 bird0.csv.gz
mv vertnet_latest_birds.csv.gz000000000001 bird1.csv.gz
mv vertnet_latest_birds.csv.gz000000000002 bird2.csv.gz
mv vertnet_latest_birds.csv.gz000000000003 bird3.csv.gz
mv vertnet_latest_birds.csv.gz000000000004 bird4.csv.gz
mv vertnet_latest_birds.csv.gz000000000005 bird5.csv.gz
mv vertnet_latest_birds.csv.gz000000000006 bird6.csv.gz
mv vertnet_latest_birds.csv.gz000000000007 bird7.csv.gz
mv vertnet_latest_birds.csv.gz000000000008 bird8.csv.gz
mv vertnet_latest_birds.csv.gz000000000009 bird9.csv.gz
mv vertnet_latest_birds.csv.gz000000000010 bird10.csv.gz
mv vertnet_latest_birds.csv.gz000000000011 bird11.csv.gz
mv vertnet_latest_birds.csv.gz000000000012 bird12.csv.gz
mv vertnet_latest_birds.csv.gz000000000013 bird13.csv.gz
mv vertnet_latest_birds.csv.gz000000000014 bird14.csv.gz
mv vertnet_latest_birds.csv.gz000000000015 bird15.csv.gz
gunzip bird*
sed '1d' bird1.csv > tmp1
sed '1d' bird2.csv > tmp2
sed '1d' bird3.csv > tmp3
sed '1d' bird4.csv > tmp4
sed '1d' bird5.csv > tmp5
sed '1d' bird6.csv > tmp6
sed '1d' bird7.csv > tmp7
sed '1d' bird8.csv > tmp8
sed '1d' bird9.csv > tmp9
sed '1d' bird10.csv > tmp10
sed '1d' bird11.csv > tmp11
sed '1d' bird12.csv > tmp12
sed '1d' bird13.csv > tmp13
sed '1d' bird14.csv > tmp14
sed '1d' bird15.csv > tmp15
cat bird0.csv tmp1 tmp2 tmp3 tmp4 tmp5 tmp6 tmp7 tmp8 tmp9 tmp10 tmp11 tmp12 tmp13 tmp14 tmp15 > vertnet_latest_birds.csv
gzip vertnet_latest_birds.csv
gsutil cp vertnet_latest_birds.csv.gz gs://vertnet-byclass/vertnet_latest_birds.csv.gz
