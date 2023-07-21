#!/bin/bash

# 定义服务器信息
push_server_name="Ops-Server"
push_server_ip="192.168.5.103"
# Webhook URL
webhook_url="https://open.feishu.cn/open-apis/bot/v2/hook/"


# 内网DNS服务器列表和昵称
declare -A inner_dns_servers=(
    ["192.168.5.88"]="VIP-A"
    ["192.168.5.188"]="VIP-B"
    ["192.168.5.101"]="主机"
    ["192.168.5.102"]="备机"
)

# 外网DNS服务器列表和昵称
declare -A outer_dns_servers=(
    ["8.8.8.8"]="GOOGLE-DNS-01"
    ["8.8.4.4"]="GOOGLE-DNS-02"
    ["114.114.114.144"]="114-DNS-CN"
    ["119.29.29.29"]="Tencent-DNS-CN"
    ["223.5.5.5"]="Ali-DNS-CN-01"
    ["223.6.6.6"]="Ali-DNS-CN-02"
    ["180.76.76.76"]="Baidu-DNS-CN"
    ["1.1.1.1"]="CloudFlare-DNS-01"
    ["1.0.0.1"]="CloudFlare-DNS-02"
    ["208.67.222.220"]="Cisco-DNS-01"
    ["208.67.222.222"]="Cisco-DNS-02"
)

# 需要检查的域名列表
inner_domains=(
    "www.blueskyxn.com"
    "cdn.000714.xyz"
    "www.fbi.gov"
    "www.usa.gov"
    "www.github.com"
)

outer_domains=(
    "www.microsoft.com"
    "www.google.com"
    "www.bilibili.com"
    "www.bing.com"
    "www.cloudflare.com"
)

# 存储结果的数组
declare -A results

# 检查函数
check_dns_servers() {
    local -n dns_servers=$1
    local check_inner=$2
    for dns in "${!dns_servers[@]}"; do
        echo "Checking ${dns_servers[$dns]} ($dns)..."
        success=0
        total=0
        total_time=0
        # 检查内网域名
        if [ $check_inner -eq 1 ]; then
            for domain in "${inner_domains[@]}"; do
                result=$(timeout 2 dig @$dns $domain +short +time=1 +tries=1)
                if [ $? -eq 0 ] && [ -n "$result" ]; then
                    success=$((success+1))
                fi
                total=$((total+1))
                # 获取查询时间
                time=$(timeout 2 dig @$dns $domain +stats 2>/dev/null | grep "Query time:" | awk '{print $4}')
                total_time=$((total_time+time))
            done
        fi
        # 检查外网域名
        for domain in "${outer_domains[@]}"; do
            result=$(timeout 2 dig @$dns $domain +short +time=1 +tries=1)
            if [ $? -eq 0 ] && [ -n "$result" ]; then
                success=$((success+1))
            fi
            total=$((total+1))
            # 获取查询时间
            time=$(timeout 2 dig @$dns $domain +stats 2>/dev/null | grep "Query time:" | awk '{print $4}')
            total_time=$((total_time+time))
        done
        # 计算成功率和平均响应时间
        avg_time=$((total_time/total))
        results[$dns]="$success/$total ${avg_time}ms"
    done
}

# 检查内网和外网DNS服务器
check_dns_servers inner_dns_servers 1
check_dns_servers outer_dns_servers 0

# 存储排序后的内网DNS服务器列表
sorted_inner_dns_servers=(
    "192.168.5.88"
    "192.168.5.188"
    "192.168.5.101"
    "192.168.5.102"
)

# 存储排序后的外网DNS服务器列表
sorted_outer_dns_servers=(
    "8.8.8.8"
    "8.8.4.4"
    "114.114.114.144"
    "119.29.29.29"
    "223.5.5.5"
    "223.6.6.6"
    "180.76.76.76"
    "1.1.1.1"
    "1.0.0.1"
    "208.67.222.220"
    "208.67.222.222"
)

# 开始构建推送消息
push_msg="\n**内网DNS服务器：**\n"

for dns in "${sorted_inner_dns_servers[@]}"; do
    if [[ ${results[$dns]+_} ]]; then
        success_rate=${results[$dns]%% *}
        avg_time=${results[$dns]#* }
        push_msg+="- ${inner_dns_servers[$dns]} ($dns) 成功率：$success_rate 平均耗时：$avg_time\n"
    fi
done

push_msg+="\n**外网DNS服务器：**\n"

for dns in "${sorted_outer_dns_servers[@]}"; do
    if [[ ${results[$dns]+_} ]]; then
        success_rate=${results[$dns]%% *}
        avg_time=${results[$dns]#* }
        push_msg+="- ${outer_dns_servers[$dns]} ($dns) 成功率：$success_rate 平均耗时：$avg_time\n"
    fi
done

# 获取当前时间（香港时间）
push_time=$(TZ=Asia/Hong_Kong date +"%Y-%m-%d %H:%M")

# 发送消息
curl -X POST -H "Content-Type: application/json" \
    -d '{
        "msg_type": "interactive",
        "card": {
            "elements": [
                {
                    "tag": "div",
                    "fields": [
                        {
                            "is_short": true,
                            "text": {
                                "tag": "lark_md",
                                "content": "**🕐 时间：**\n'"$push_time"'"
                            }
                        },
                        {
                            "is_short": true,
                            "text": {
                                "tag": "lark_md",
                                "content": "**🖥️服务器信息：**\n 名称：'"$push_server_name"' <font color=red>|</font> IP：'"$push_server_ip"'"
                            }
                        }
                    ]
                },
                {
                    "tag": "markdown",
                    "content": "💣通知详情：'"$push_msg"'"
                }
            ],
            "header": {
                "template": "blue",
                "title": {
                    "content": "【DNS】状态监测报告|每小时运行一次",
                    "tag": "plain_text"
                }
            }
        }
    }' \
    $webhook_url
