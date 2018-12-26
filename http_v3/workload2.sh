#! /bin/sh
#
# Stimulate storage access workload
#

rm -f workload.log statPcap.txt

files=(
	"dir1/1.txt" "dir1/2.txt" "dir1/3.txt" \
	"dir2/dir2_subdir/4.txt" "dir2/dir2_subdir/5.txt" "dir2/dir2_subdir/6.txt" \
	"dir3/dir3_subdir/dir3_subdir_subdir/7.txt" "dir3/dir3_subdir/dir3_subdir_subdir/8.txt" "dir3/dir3_subdir/dir3_subdir_subdir/9.txt"\
)

for i in {1..10}; do
  f=$[$RANDOM%9]
  url="http://10.30.31.1/${files[$f]}"
  curl ${url} &>/dev/null
  # echo "$(date) GET $url" >> workload.log
done

killall tcpdump

