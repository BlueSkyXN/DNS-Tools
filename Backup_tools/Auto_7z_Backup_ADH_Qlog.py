import datetime
import subprocess
import os
import shutil
import tempfile
import configparser
import requests
import json
import argparse

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

def create_backup(config_path):
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(config_path)

    source_file = config.get('DEFAULT', 'SourceFile')
    backup_dir = config.get('DEFAULT', 'BackupDir')
    webhook_url = config.get('DEFAULT', 'WebhookURL')
    backup_file_prefix = config.get('DEFAULT', 'BackupFileNamePrefix')
    notification_message_prefix = config.get('DEFAULT', 'NotificationMessagePrefix')
    sevenz_path = config.get('DEFAULT', 'SevenZPath')

    # 获取当前时间
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m%d-%H%M")

    # 构建备份文件名
    backup_file = backup_file_prefix + formatted_time + ".7z"

    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 构建临时文件名
        temp_file = os.path.join(temp_dir, backup_file_prefix + formatted_time + ".json")

        # 复制源文件到临时文件并重命名
        shutil.copy(source_file, temp_file)

        # 使用7z命令创建压缩文件
        subprocess.run([sevenz_path, "a", backup_dir + backup_file, temp_file, "-mx9", "-mmt4"])

    print(f"{notification_message_prefix} {backup_file}")
    NotifytoWebhook(webhook_url, f"{notification_message_prefix} {backup_file}")

if __name__ == "__main__":
    # 创建解析器
    parser = argparse.ArgumentParser(description='Backup files and notify via webhook.')
    # 添加-c --config 参数
    parser.add_argument('-c', '--config', type=str, default='backup-config.ini',
                        help='Path to the configuration file')
    # 解析命令行参数
    args = parser.parse_args()

    # 调用create_backup函数，并传入配置文件路径
    create_backup(args.config)
