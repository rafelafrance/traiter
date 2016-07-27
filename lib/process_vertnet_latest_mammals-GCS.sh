#!/usr/bin/bash
rm tmp*
rm mam*.csv
rm vertnet_latest_mam*
gsutil cp gs://vertnet-byclass/vertnet_latest_mammals* .
mv vertnet_latest_mammals.csv.gz000000000000 mamm0.csv.gz
mv vertnet_latest_mammals.csv.gz000000000001 mamm1.csv.gz
mv vertnet_latest_mammals.csv.gz000000000002 mamm2.csv.gz
mv vertnet_latest_mammals.csv.gz000000000003 mamm3.csv.gz
mv vertnet_latest_mammals.csv.gz000000000004 mamm4.csv.gz
mv vertnet_latest_mammals.csv.gz000000000005 mamm5.csv.gz
mv vertnet_latest_mammals.csv.gz000000000006 mamm6.csv.gz
mv vertnet_latest_mammals.csv.gz000000000007 mamm7.csv.gz
mv vertnet_latest_mammals.csv.gz000000000008 mamm8.csv.gz
mv vertnet_latest_mammals.csv.gz000000000009 mamm9.csv.gz
mv vertnet_latest_mammals.csv.gz000000000010 mamm10.csv.gz
mv vertnet_latest_mammals.csv.gz000000000011 mamm11.csv.gz
gunzip mamm*
sed '1d' mamm1.csv > tmp1
sed '1d' mamm2.csv > tmp2
sed '1d' mamm3.csv > tmp3
sed '1d' mamm4.csv > tmp4
sed '1d' mamm5.csv > tmp5
sed '1d' mamm6.csv > tmp6
sed '1d' mamm7.csv > tmp7
sed '1d' mamm8.csv > tmp8
sed '1d' mamm9.csv > tmp9
sed '1d' mamm10.csv > tmp10
sed '1d' mamm11.csv > tmp11
cat mamm0.csv tmp1 tmp2 tmp3 tmp4 tmp5 tmp6 tmp7 tmp8 tmp9 tmp10 tmp11 > vertnet_latest_mammals.csv
gzip vertnet_latest_mammals.csv
gsutil cp vertnet_latest_mammals.csv.gz gs://vertnet-byclass/vertnet_latest_mammals.csv.gz
