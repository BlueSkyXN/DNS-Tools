#!/bin/bash
#echo "First argument: $1" >> /etc/keepalived/notify.log
#echo "Second argument: $2" >> /etc/keepalived/notify.log

# 飞书Webhook机器人的URL
WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/"

# 通过命令行参数获取通知类型和状态
# 通知类型可为 "notify"
# 状态为 "master", "backup", 或 "fault"
NOTIFY_TYPE=$1
STATUS=$2

# 本地名称和IP地址
LOCAL_NAME="DNS-Server"
LOCAL_IP="192.168.5.1"

# 获取当前时间
push_time=$(date -u -d "+8 hours" +"%Y-%m-%d %H:%M")

# 定义通知函数
notify() {
    local type=$1
    local status=$2

    # 在这里根据不同的通知类型和状态执行相应的操作
    if [[ $type == "notify" && $status == "master" ]]; then
        # 当该机器成为 MASTER 时执行的操作
        message="该机器现在是主服务器(MAIN/MASTER)"
        # 可以根据需要自定义消息内容

    elif [[ $type == "notify" && $status == "backup" ]]; then
        # 当该机器成为 BACKUP 时执行的操作
        message="该机器现在是备服务器(BACK/BACKUP)"
        # 可以根据需要自定义消息内容

    else
        message="发生错误, 未知的通知类型或状态。"
    fi

    # 发送通知到飞书
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
                                    "content": "**🖥️服务器信息：**\n 名称：'"$LOCAL_NAME"' <font color=red>|</font> IP：'"$LOCAL_IP"'"
                                }
                            }
                        ]
                    },
                    {
                        "tag": "markdown",
                        "content": "💣通知详情：'"$message"'"
                    },
                    {
                        "tag": "column_set",
                        "flex_mode": "none",
                        "background_style": "default",
                        "columns": []
                    },
                    {
                        "tag": "column_set",
                        "flex_mode": "none",
                        "background_style": "default",
                        "columns": []
                    }
                ],
                "header": {
                    "template": "red",
                    "title": {
                        "content": "【DNS】通知",
                        "tag": "plain_text"
                    }
                }
            }
        }' \
        $WEBHOOK_URL
}

# 调用通知函数
notify $NOTIFY_TYPE $STATUS
