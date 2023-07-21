#!/bin/bash
LOGFILE="/etc/keepalived/keepalived.log" #指定 log文件
case "$1" in
check)
    ALIVE=0
    ALIVE=$(dig www.feishu.cn @$2 |grep "NOERROR")
    if [ $? == 0 ]; then
        #echo "啥也不是.ALIVE" >>$LOGFILE # 双箭是追加，单箭是覆盖
        #echo $ALIVE >>$LOGFILE #日志可不写
        exit 0 #状态正常
    else
        #echo "FAIL.翻车兄弟们" >>$LOGFILE
        #echo $ALIVE >>$LOGFILE #日志可不写
        exit 1 #状态异常
    fi
    ;;
    *)
    ;;
notify)
    #通告，下面不能乱动，保持啥也不干
    #echo "啥也不是.NOTIFY" >>$LOGFILE
    ;;
esac