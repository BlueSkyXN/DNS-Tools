#!/bin/bash

# Variables
push_server_name="WEB-Server"
push_server_ip="192.168.5.103"
check_server_name="DNS-VIP"
check_server_ip="192.168.5.88"
webhook_url="https://open.feishu.cn/open-apis/bot/v2/hook/"
debug=false

# Check DNS
dig_result=$(dig @${check_server_ip} www.feishu.cn +timeout=5 +retry=2)

# Check if dig command succeeded
if [ $? -ne 0 ] || [ -z "$dig_result" ]; then
    # Dig command failed
    push_msg="【故障】DNS FAIL at $check_server_ip"
else
    # Dig command succeeded
    push_msg="【正常】DNS OK at $check_server_ip"
    if [ "$debug" = false ]; then
        # If debug is off, we don't push the success message
        #echo "Dig command succeeded and debug is off, exiting without pushing a message."
        exit 0
    fi
fi

# Prepare the JSON payload
json_payload=$(cat <<EOF
{
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
              "content": "**🕐 时间：**\n$(date)"
            }
          },
          {
            "is_short": true,
            "text": {
              "tag": "lark_md",
              "content": "**🖥️本地服务器信息：**\n 名称：$push_server_name <font color=red>|</font> IP：$push_server_ip"
            }
          }
        ]
      },
      {
        "tag": "markdown",
        "content": "**🖥️检测对象信息：**\n 名称：$check_server_name <font color=red>|</font> IP：$check_server_ip"
      },
      {
        "tag": "markdown",
        "content": "💣通知详情：$push_msg"
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
        "content": "【DNS】运维通知",
        "tag": "plain_text"
      }
    }
  }
}
EOF
)

# Send the POST request
curl -X POST -H "Content-Type: application/json" -d "$json_payload" $webhook_url
