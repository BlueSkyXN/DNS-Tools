#!/bin/bash

# 定义用于检测的域名和子网
DOMAIN="www.cloudflare.com"
SUBNET="110.110.110.0/24"

# 初始化参数变量
SKIP_IPV4=0
SKIP_IPV6=0
MAX_CONCURRENCY=10  # 最大并发数

# 解析命令行参数
while getopts "46" opt; do
  case ${opt} in
    4 ) SKIP_IPV6=1 ;;
    6 ) SKIP_IPV4=1 ;;
    \? ) echo "Usage: cmd [-4] [-6]"; exit 1 ;;
  esac
done

# 创建一个临时文件来存储结果
TEMP_RESULT=$(mktemp)

# 定义处理每个 DNS IP 的函数
process_dns_ip() {
    local line=$1
    local ecs_support="No"
    local latency="999"
    local query_success="No"
    local output_line

    if [[ $SKIP_IPV4 -eq 1 && $line =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        ecs_support="PASS"
        query_success="PASS"
        latency="PASS"
    elif [[ $SKIP_IPV6 -eq 1 && $line =~ ^[0-9a-fA-F:]+$ ]]; then
        ecs_support="PASS"
        query_success="PASS"
        latency="PASS"
    else
        for i in {1..3}; do
            DIG_OUTPUT=$(dig @$line $DOMAIN +subnet=$SUBNET +noall +comments +stats +tries=1 +retry=1)
            if echo "$DIG_OUTPUT" | grep -q "status: NOERROR"; then
                query_success="Yes"
                RESULT=$(echo "$DIG_OUTPUT" | grep "CLIENT-SUBNET")
                LATENCY=$(echo "$DIG_OUTPUT" | grep "Query time" | grep -oP '\d+(?= msec)')
                ecs_support=$([[ -n "$RESULT" ]] && echo "Yes" || echo "No")
                break
            fi
            sleep 1
        done
        latency=${LATENCY:-"N/A"}
    fi

    output_line="$line | $ecs_support | $query_success | $latency"
    echo "$output_line" >> "$TEMP_RESULT"
}

# 读取 dns-ip.txt 文件并并发处理每行
while IFS= read -r line; do
    process_dns_ip "$line" &
    if (( $(jobs -p | wc -l) >= MAX_CONCURRENCY )); then
        wait
    fi
done < "dns-ip.txt"

wait  # 确保所有后台进程都已完成

# 打印表头并输出结果
{
    printf "%-20s | %-12s | %-15s | %-s\n" "DNS IP" "ECS Support" "Query Success" "Latency (ms)"
    echo "---------------------|--------------|-----------------|----------------"
    cat "$TEMP_RESULT"
} | tee >(awk -F ' | ' '{print $1","$3","$5","$7}' > dns_check_results.csv)

rm "$TEMP_RESULT"  # 清理临时文件
echo "Results have been saved to dns_check_results.csv"
