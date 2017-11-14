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
mv vertnet_latest_mammals.csv.gz000000000012 mamm12.csv.gz
mv vertnet_latest_mammals.csv.gz000000000013 mamm13.csv.gz
mv vertnet_latest_mammals.csv.gz000000000014 mamm14.csv.gz
mv vertnet_latest_mammals.csv.gz000000000015 mamm15.csv.gz
mv vertnet_latest_mammals.csv.gz000000000016 mamm16.csv.gz
mv vertnet_latest_mammals.csv.gz000000000017 mamm17.csv.gz
mv vertnet_latest_mammals.csv.gz000000000018 mamm18.csv.gz
mv vertnet_latest_mammals.csv.gz000000000019 mamm19.csv.gz
mv vertnet_latest_mammals.csv.gz000000000020 mamm20.csv.gz
mv vertnet_latest_mammals.csv.gz000000000021 mamm21.csv.gz
mv vertnet_latest_mammals.csv.gz000000000022 mamm22.csv.gz
mv vertnet_latest_mammals.csv.gz000000000023 mamm23.csv.gz
mv vertnet_latest_mammals.csv.gz000000000024 mamm24.csv.gz
mv vertnet_latest_mammals.csv.gz000000000025 mamm25.csv.gz
mv vertnet_latest_mammals.csv.gz000000000026 mamm26.csv.gz
mv vertnet_latest_mammals.csv.gz000000000027 mamm27.csv.gz
mv vertnet_latest_mammals.csv.gz000000000028 mamm28.csv.gz
mv vertnet_latest_mammals.csv.gz000000000029 mamm29.csv.gz
mv vertnet_latest_mammals.csv.gz000000000030 mamm30.csv.gz
mv vertnet_latest_mammals.csv.gz000000000031 mamm31.csv.gz
mv vertnet_latest_mammals.csv.gz000000000032 mamm32.csv.gz
mv vertnet_latest_mammals.csv.gz000000000033 mamm33.csv.gz
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
sed '1d' mamm12.csv > tmp12
sed '1d' mamm13.csv > tmp13
sed '1d' mamm14.csv > tmp14
sed '1d' mamm15.csv > tmp15
sed '1d' mamm16.csv > tmp16
sed '1d' mamm17.csv > tmp17
sed '1d' mamm18.csv > tmp18
sed '1d' mamm19.csv > tmp19
sed '1d' mamm20.csv > tmp20
sed '1d' mamm21.csv > tmp21
sed '1d' mamm22.csv > tmp22
sed '1d' mamm23.csv > tmp23
sed '1d' mamm24.csv > tmp24
sed '1d' mamm25.csv > tmp25
sed '1d' mamm26.csv > tmp26
sed '1d' mamm27.csv > tmp27
sed '1d' mamm28.csv > tmp28
sed '1d' mamm29.csv > tmp29
sed '1d' mamm30.csv > tmp30
sed '1d' mamm31.csv > tmp31
sed '1d' mamm32.csv > tmp32
sed '1d' mamm33.csv > tmp33
cat mamm0.csv tmp1 tmp2 tmp3 tmp4 tmp5 tmp6 tmp7 tmp8 tmp9 tmp10 tmp11 tmp12 tmp13 tmp14 tmp15 tmp16 tmp17 tmp18 tmp19 tmp20 tmp21 tmp22 tmp23 tmp24 tmp25 tmp26 tmp27 tmp28 tmp29 tmp30 tmp31 tmp32 tmp33 > vertnet_latest_mammals.csv
gzip vertnet_latest_mammals.csv
gsutil cp vertnet_latest_mammals.csv.gz gs://vertnet-byclass/vertnet_latest_mammals.csv.gz
