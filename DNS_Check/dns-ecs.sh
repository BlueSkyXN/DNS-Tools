#!/bin/bash

# 定义用于检测的域名和子网
DOMAIN="www.cloudflare.com"
SUBNET="110.110.110.0/24"

# 初始化参数变量
SKIP_IPV4=0
SKIP_IPV6=0

# 解析命令行参数
while getopts "46" opt; do
  case ${opt} in
    4 ) SKIP_IPV6=1 ;;
    6 ) SKIP_IPV4=1 ;;
    \? ) echo "Usage: cmd [-4] [-6]"; exit 1 ;;
  esac
done

# 打印表头
printf "%-20s | %-12s | %-s\n" "DNS IP" "ECS Support" "Latency (ms)"
echo "---------------------|--------------|----------------"

# CSV 文件头部
echo "DNS IP,ECS Support,Latency (ms)" > dns_check_results.csv

# 读取同目录下的 dns-ip.txt 文件中的每个 IP 地址
while IFS= read -r line; do
    # 初始化 ECS_SUPPORT 为 'No' 和 LATENCY 为 '999'
    ECS_SUPPORT="No"
    LATENCY="999"

    # 根据参数决定是否跳过某类型的 IP 地址，并将其标记为 'PASS'
    if [[ $SKIP_IPV4 -eq 1 && $line =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        ECS_SUPPORT="PASS"
    elif [[ $SKIP_IPV6 -eq 1 && $line =~ ^[0-9a-fA-F:]+$ ]]; then
        ECS_SUPPORT="PASS"
    else
        # 使用 dig 命令检查当前 DNS IP 是否支持 ECS 并获取延迟
        DIG_OUTPUT=$(dig @$line $DOMAIN +subnet=$SUBNET +noall +comments +stats)
        RESULT=$(echo "$DIG_OUTPUT" | grep "CLIENT-SUBNET")
        LATENCY=$(echo "$DIG_OUTPUT" | grep "Query time" | grep -oP '\d+(?= msec)')

        # 判断是否找到了包含 "CLIENT-SUBNET" 字样的行，以此判断是否支持 ECS
        if [[ -n "$RESULT" ]]; then
            ECS_SUPPORT="Yes"
        fi

        # 如果没有获取到 LATENCY，设为 'N/A'
        if [[ -z "$LATENCY" ]]; then
            LATENCY="N/A"
        fi
    fi

    # 打印当前 DNS IP 及其 ECS 支持情况和延迟
    printf "%-20s | %-12s | %-s\n" "$line" "$ECS_SUPPORT" "$LATENCY"

    # 将相同的信息写入到 CSV 文件中
    echo "$line,$ECS_SUPPORT,$LATENCY" >> dns_check_results.csv

done < "dns-ip.txt"

echo "Results have been saved to dns_check_results.csv"
