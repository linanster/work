#! /bin/sh
#
# Stimulate storage access workload
#

rm -f workload.log statPcap.txt

files=("1.txt" "2.txt" "3.txt" "4.txt")
for i in {1..10}; do
  f=$[$RANDOM%4]
  url="http://10.30.31.1/${files[$f]}"
  curl ${url} &>/dev/null
  # echo "$(date) GET $url" >> workload.log
done

killall tcpdump

