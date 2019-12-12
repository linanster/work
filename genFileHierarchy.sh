#!/usr/bin/env sh
#

WORKDIR=$(cd $(dirname $0) && pwd)

# limitation
declare -i MAX_FILE_COUNT=1000
declare -i MAX_WIDTH=3
declare -i MAX_DEPTH=3
# counter
declare -i cur_file_count=0
declare -i cur_depth=1

usage=$"
Usage:
gen.sh -w <max_width> -d <max_depth> -m <max_file_counts>

Default:
  max_width: ${MAX_WIDTH}
  max_depth: ${MAX_DEPTH}
  max_file_counts: ${MAX_FILE_COUNT}

"

# statistic sum file counts
function statistics(){
  echo "done!"
  echo "file number: ${cur_file_count}"
}

# get a random time string used for "touch -t" command, like "201409170632"
function get_filetime(){
  year=201$[$RANDOM%10]
  month=$[$RANDOM%12+1]
  [ $month -lt 10 ] && { month=0$month; }
  day=$[$RANDOM%28+1]
  [ $day -lt 10 ] && { day=0$day; }
  hour=$[$RANDOM%24]
  [ $hour -lt 10 ] && { hour=0$hour; }
  min=$[$RANDOM%60]
  [ $min -lt 10 ] && { min=0$min; }
  echo "$year$month$day$hour$min"
}

# 创建一个文件夹
function createfolder(){
  FOLDERNAME=folder-${RANDOM}
  mkdir ${FOLDERNAME}
}
# 创建随机数量的文件夹(不超过MAX_WIDTH)
function createfolders(){
  WIDTH=$[$RANDOM%$MAX_WIDTH+1]
  for i in $(seq 1 ${WIDTH}); do
    createfolder
  done
}
# 创建一个随机大小，随机时间的文件
function createfile(){
    [ $cur_file_count -ge $MAX_FILE_COUNT ] && { echo "exceed MAX_FILE_COUNT $MAX_FILE_COUNT"; statistics; exit 1; }
    FILENAME=file-${RANDOM}
    FILESIZE=$[${RANDOM}%100]
    FILETIME="$(get_filetime)"
    dd if=/dev/zero of=${FILENAME} bs=1 count=${FILESIZE} &>/dev/null
    touch -t "$FILETIME" ${FILENAME}
    let cur_file_count++
}
# 创建随机数量的文件(不超过MAX_WIDTH_COUNT)
function createfiles(){
  WIDTH=$[$RANDOM%$MAX_WIDTH+1]
  for i in $(seq 1 ${WIDTH}); do
    createfile
  done
}

gen_folders(){
  # 先创建目录
  if [ $cur_depth -le $MAX_DEPTH ]; then
    createfolders
  else
     return
  fi
  # 遍历刚刚创建的目录
  folderlist=$(ls -1)
  for folder in $folderlist; do
    # 进入目录，递归创建目录
    cd $folder
    cur_depth=$[$cur_depth+1]
    gen_folders
    cd ..
    cur_depth=$[$cur_depth-1]
  done
}

gen_files(){
  filelist=`ls -1`
  if [ -z "$filelist" ]
  # 当前目录为空时，表示进入最内层目录，创建文件
  then
    createfiles
  # 当前目录不为空时，遍历每个子目录（忽略文件）
  else
    for filename in $filelist
    do
      if test -d $filename  # 检查是否是目录
      then
        # 进入每个子目录，递归创建文件
        cd $filename
        gen_files
        cd ..
      fi
    done
    createfiles
  fi
}

# read parameter
while [ $# -ge 1 ]; do
    case $1 in
      --help|-h)
        printf "$usage"
        exit 0
        ;;
      -w)
        MAX_WIDTH=$2
        ;;
      -d)
        MAX_DEPTH=$2
        ;;
      -m)
        MAX_FILE_COUNT=$2
        ;;
      *)
        printf "$usage"
        exit 1
        ;;
    esac
    shift && shift || true
done
        
      


# start work from cd workdir, this is a good hobby.
cd ${WORKDIR}
[ -d rootdir ] && mv rootdir rootdir_$(date "+%Y%m%d%H%M%S")
mkdir rootdir && cd rootdir || exit

# generate folder tree
gen_folders

# generate random files among this tree
cd ${WORKDIR}/rootdir
gen_files

statistics

