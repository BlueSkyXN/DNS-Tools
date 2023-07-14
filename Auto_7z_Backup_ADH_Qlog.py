import datetime
import subprocess
import os
import shutil
import tempfile
import configparser
from Notify_to_Webhook import NotifytoWebhook

def create_backup():
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read('backup-config.ini')

    source_file = config.get('DEFAULT', 'SourceFile')
    backup_dir = config.get('DEFAULT', 'BackupDir')
    webhook_url = config.get('DEFAULT', 'WebhookURL')
    backup_file_prefix = config.get('DEFAULT', 'BackupFileNamePrefix')
    notification_message_prefix = config.get('DEFAULT', 'NotificationMessagePrefix')

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
        subprocess.run(["7z", "a", backup_dir + backup_file, temp_file])

    print(f"{notification_message_prefix} {backup_file}")
    NotifytoWebhook(webhook_url, f"{notification_message_prefix} {backup_file}")

if __name__ == "__main__":
    create_backup()
