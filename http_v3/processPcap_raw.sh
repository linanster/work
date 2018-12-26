#! /bin/bash
#
# Read pcap file, parse, and then write formatted data to MySQL.
#

if [ 1 -ne $# ]; then
  echo "Usage: processPcap.sh <pcapfile>"
  exit 1
fi

declare TIMESTAMP CLIENTIP TARGETIP SEQ ACK DETAIL

tcpdump -Snn -r $1 | while read LINE; do
  TIMESTAMP=$(echo ${LINE} | awk '{print $1}')
  CLIENTIP=$(echo ${LINE} | awk '{print $3}' | awk 'BEGIN{FS="."}{printf "%s.%s.%s.%s", $1,$2,$3,$4}')
  TARGETIP=$(echo ${LINE} | awk '{print $5}' | awk 'BEGIN{FS="."}{printf "%s.%s.%s.%s", $1,$2,$3,$4}')
  SEQ=$(echo $LINE | awk 'BEGIN{FS="seq"}{print $2}' | awk 'BEGIN{FS=":"}{print $1}')
  ACK=$(echo ${LINE} | awk 'BEGIN{FS="ack"}{print $2}' | awk 'BEGIN{FS=","}{print $1}' | awk '{print $1}')
  DETAIL=$(echo ${LINE} | awk 'BEGIN{FS="HTTP: "}{print $2}')
  # echo ${TIMESTAMP} ${CLIENTIP} ${TARGETIP} ${SEQ} ${ACK} ${DETAIL}
  
  sql_insert="INSERT INTO test.data_pcap_raw values(\"${TIMESTAMP}\",\"${CLIENTIP}\",\"${TARGETIP}\",${SEQ},${ACK},\"${DETAIL}\");"
  # echo ${sql_insert}
  mysql -h10.30.30.121 -uroot -e "${sql_insert}"
# done < 3.txt
done
