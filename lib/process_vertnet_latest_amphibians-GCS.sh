#!/usr/bin/bash
rm tmp*
rm amph*.csv
rm vertnet_latest_amphibians*
gsutil cp gs://vertnet-byclass/vertnet_latest_amphibians* .
mv vertnet_latest_amphibians.csv.gz000000000000 amph0.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000001 amph1.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000002 amph2.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000003 amph3.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000004 amph4.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000005 amph5.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000006 amph6.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000007 amph7.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000008 amph8.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000009 amph9.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000010 amph10.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000011 amph11.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000012 amph12.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000013 amph13.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000014 amph14.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000015 amph15.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000016 amph16.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000017 amph17.csv.gz
mv vertnet_latest_amphibians.csv.gz000000000018 amph18.csv.gz
gunzip amph*
sed '1d' amph1.csv > tmp1
sed '1d' amph2.csv > tmp2
sed '1d' amph3.csv > tmp3
sed '1d' amph4.csv > tmp4
sed '1d' amph5.csv > tmp5
sed '1d' amph6.csv > tmp6
sed '1d' amph7.csv > tmp7
sed '1d' amph8.csv > tmp8
sed '1d' amph9.csv > tmp9
sed '1d' amph10.csv > tmp10
sed '1d' amph11.csv > tmp11
sed '1d' amph12.csv > tmp12
sed '1d' amph13.csv > tmp13
sed '1d' amph14.csv > tmp14
sed '1d' amph15.csv > tmp15
sed '1d' amph16.csv > tmp16
sed '1d' amph17.csv > tmp17
sed '1d' amph18.csv > tmp18
cat amph0.csv tmp1 tmp2 tmp3 tmp4 tmp5 tmp6 tmp7 tmp8 tmp9 tmp10 tmp11 tmp12 tmp13 tmp14 tmp15 tmp16 tmp17 tmp18 > vertnet_latest_amphibians.csv
gzip vertnet_latest_amphibians.csv
gsutil cp vertnet_latest_amphibians.csv.gz gs://vertnet-byclass/vertnet_latest_amphibians.csv.gz
