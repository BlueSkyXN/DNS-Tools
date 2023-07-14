import requests
import json

def NotifytoWebhook(webhook_url, message):
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }

    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print("Failed to send message. Response code:", response.status_code)


# 测试函数
webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/"
message = "Notify-to-Webhook.py TEST"

NotifytoWebhook(webhook_url, message)
