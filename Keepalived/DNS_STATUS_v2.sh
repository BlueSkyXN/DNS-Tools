#!/bin/bash
LOGFILE="/etc/keepalived/keepalived.log" #指定 log 文件
case "$1" in
check)
    ALIVE=$(dig +short www.feishu.cn @$2)
    if [ $? -eq 0 ]; then
        echo "域名解析正常: $ALIVE" >> $LOGFILE
        exit 0 # 状态正常
    else
        echo "域名解析失败" >> $LOGFILE
        exit 1 # 状态异常
    fi
    ;;
notify)
    # 通告，下面不能乱动，保持啥也不干
    echo "通告: NOTIFY" >> $LOGFILE
    ;;
*)
    echo "无效的参数：$1" >> $LOGFILE
    exit 1
    ;;
esac
