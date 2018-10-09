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
mv vertnet_latest_birds.csv.gz000000000016 bird16.csv.gz
mv vertnet_latest_birds.csv.gz000000000017 bird17.csv.gz
mv vertnet_latest_birds.csv.gz000000000018 bird18.csv.gz
mv vertnet_latest_birds.csv.gz000000000019 bird19.csv.gz
mv vertnet_latest_birds.csv.gz000000000020 bird20.csv.gz
mv vertnet_latest_birds.csv.gz000000000021 bird21.csv.gz
mv vertnet_latest_birds.csv.gz000000000022 bird22.csv.gz
mv vertnet_latest_birds.csv.gz000000000023 bird23.csv.gz
mv vertnet_latest_birds.csv.gz000000000024 bird24.csv.gz
mv vertnet_latest_birds.csv.gz000000000025 bird25.csv.gz
mv vertnet_latest_birds.csv.gz000000000026 bird26.csv.gz
mv vertnet_latest_birds.csv.gz000000000027 bird27.csv.gz
mv vertnet_latest_birds.csv.gz000000000028 bird28.csv.gz
mv vertnet_latest_birds.csv.gz000000000029 bird29.csv.gz
mv vertnet_latest_birds.csv.gz000000000030 bird30.csv.gz
mv vertnet_latest_birds.csv.gz000000000031 bird31.csv.gz
mv vertnet_latest_birds.csv.gz000000000032 bird32.csv.gz
mv vertnet_latest_birds.csv.gz000000000033 bird33.csv.gz
mv vertnet_latest_birds.csv.gz000000000034 bird34.csv.gz
mv vertnet_latest_birds.csv.gz000000000035 bird35.csv.gz
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
sed '1d' bird16.csv > tmp16
sed '1d' bird17.csv > tmp17
sed '1d' bird18.csv > tmp18
sed '1d' bird19.csv > tmp19
sed '1d' bird20.csv > tmp20
sed '1d' bird21.csv > tmp21
sed '1d' bird22.csv > tmp22
sed '1d' bird23.csv > tmp23
sed '1d' bird24.csv > tmp24
sed '1d' bird25.csv > tmp25
sed '1d' bird26.csv > tmp26
sed '1d' bird27.csv > tmp27
sed '1d' bird28.csv > tmp28
sed '1d' bird29.csv > tmp29
sed '1d' bird30.csv > tmp30
sed '1d' bird31.csv > tmp31
sed '1d' bird32.csv > tmp32
sed '1d' bird33.csv > tmp33
sed '1d' bird34.csv > tmp34
sed '1d' bird35.csv > tmp35
cat bird0.csv tmp1 tmp2 tmp3 tmp4 tmp5 tmp6 tmp7 tmp8 tmp9 tmp10 tmp11 tmp12 tmp13 tmp14 tmp15 tmp16 tmp17 tmp18 tmp19 tmp20 tmp21 tmp22 tmp23 tmp24 tmp25 tmp26 tmp27 tmp28 tmp29 tmp30 tmp31 tmp32 tmp33 tmp34 tmp15 > vertnet_latest_birds.csv
gzip vertnet_latest_birds.csv
gsutil cp vertnet_latest_birds.csv.gz gs://vertnet-byclass/vertnet_latest_birds.csv.gz
