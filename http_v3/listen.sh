#!/bin/sh

rm -f workload.pcap

#tcpdump -i ens35 -nn -w ./workload.pcap 'tcp and port 80 and host 10.30.31.121 and host 10.30.31.1'

tcpdump -i ens35 -nn -w ./workload.pcap 'tcp and port 80 and host 10.30.31.121 and host 10.30.31.1 and (tcp[32:2]=0x4745 or tcp[32:2]=0x4854)'
