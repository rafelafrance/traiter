#!/usr/bin/bash
rm tmp*
rm amph*.csv
rm vertnet_latest_amph*
gsutil cp gs://vertnet-byclass/vertnet_latest_amphibians* .
mv vertnet_latest_amphibians.csv.gz000000000000 amph0.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000001 amph1.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000002 amph2.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000003 amph3.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000004 amph4.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000005 amph5.csv.gz
gunzip amph*
sed '1d' amph1.csv > tmp1
sed '1d' amph2.csv > tmp2
sed '1d' amph3.csv > tmp3
sed '1d' amph4.csv > tmp4
sed '1d' amph5.csv > tmp5
cat amph0.csv tmp1 tmp2 tmp3 tmp4 tmp5 > vertnet_latest_amphibians.csv
gzip vertnet_latest_amphibians.csv
gsutil cp vertnet_latest_amphibians.csv.gz gs://vertnet-byclass/vertnet_latest_amphibians.csv.gz
