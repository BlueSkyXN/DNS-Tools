import datetime
import subprocess
import os
import shutil
import tempfile

def create_backup():
    source_file = "/opt/adh/AdGuardHome/data/querylog.json"
    backup_dir = "/opt/adh/AdGuardHome/data/backup/"

    # 获取当前时间
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m%d-%H%M")

    # 构建备份文件名
    backup_file = "querylog-backup-" + formatted_time + ".7z"

    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 构建临时文件名
        temp_file = os.path.join(temp_dir, "querylog-backup-" + formatted_time + ".json")

        # 复制源文件到临时文件并重命名
        shutil.copy(source_file, temp_file)

        # 使用7z命令创建压缩文件
        subprocess.run(["7z", "a", backup_dir + backup_file, temp_file])

    print("备份文件已创建：", backup_file)

if __name__ == "__main__":
    create_backup()
