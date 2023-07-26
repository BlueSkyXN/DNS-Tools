import paramiko

from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QGroupBox, QFormLayout, QMenuBar, QMenu, QAction, QPlainTextEdit, QInputDialog, QComboBox, QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt
import sys
import json


class SSHClient:
    def __init__(self, host, username, password):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, username=username, password=password)

    def execute(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        result = stdout.read()
        if not result:
            result = stderr.read()
        return result.decode()

    def close(self):
        self.ssh.close()


class Config:
    # 这是一个处理配置文件的类，我们会在这里实现读取和写入配置文件的功能
    print


class ConfigDialog_v1(QDialog):
    def __init__(self, parent=None):
        super(ConfigDialog_v1, self).__init__(parent)

        self.setWindowTitle("配置信息")

        self.config_layout = QFormLayout()

        self.ssh_user = QLineEdit()
        self.ssh_password = QLineEdit()
        self.ssh_password.setEchoMode(QLineEdit.Password)
        self.adh_path = QLineEdit()

        self.config_layout.addRow(QLabel("SSH用户名:"), self.ssh_user)
        self.config_layout.addRow(QLabel("SSH密码:"), self.ssh_password)
        self.config_layout.addRow(QLabel("AdGuardHome路径:"), self.adh_path)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        self.config_layout.addRow(self.buttons)

        self.setLayout(self.config_layout)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)

        self.setWindowTitle("配置信息")

        self.config_layout = QFormLayout()

        self.ssh_user = QLineEdit("root")
        self.ssh_password = QLineEdit()
        self.adh_path = QLineEdit("/opt/adh/AdGuardHome")

        self.config_layout.addRow(QLabel("SSH用户名:"), self.ssh_user)
        self.config_layout.addRow(QLabel("SSH密码:"), self.ssh_password)
        self.config_layout.addRow(QLabel("AdGuardHome路径:"), self.adh_path)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        self.config_layout.addRow(self.buttons)

        self.setLayout(self.config_layout)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("DNS管理工具")

        # 设置窗口的布局
        self.main_layout = QVBoxLayout()

        # 设置命令执行区域
        self.command_group = QGroupBox("命令执行")
        self.command_layout = QGridLayout()
        self.command_group.setLayout(self.command_layout)

        # AdGuardHome command buttons
        self.adh_start_button = QPushButton("启动AdGuardHome")
        self.adh_stop_button = QPushButton("停止AdGuardHome")
        self.adh_restart_button = QPushButton("重启AdGuardHome")
        self.adh_status_button = QPushButton("查询AdGuardHome状态")
        self.adh_pid_button = QPushButton("查询AdGuardHome PID")
        self.adh_kill_button = QPushButton("强制终止AdGuardHome")

        # AdGuardHome buttons
        self.adh_start_button.clicked.connect(self.start_adh)
        self.adh_stop_button.clicked.connect(self.stop_adh)
        self.adh_restart_button.clicked.connect(self.restart_adh)
        self.adh_status_button.clicked.connect(self.status_adh)
        self.adh_pid_button.clicked.connect(self.pid_adh)
        self.adh_kill_button.clicked.connect(self.kill_adh)

        # keepalived command buttons
        self.keep_start_button = QPushButton("启动keepalived")
        self.keep_stop_button = QPushButton("停止keepalived")
        self.keep_restart_button = QPushButton("重启keepalived")
        self.keep_status_button = QPushButton("查询keepalived状态")
        self.keep_pid_button = QPushButton("查询keepalived PID")
        self.keep_kill_button = QPushButton("强制终止keepalived")

        # keepalived buttons
        self.keep_start_button.clicked.connect(self.start_keep)
        self.keep_stop_button.clicked.connect(self.stop_keep)
        self.keep_restart_button.clicked.connect(self.restart_keep)
        self.keep_status_button.clicked.connect(self.status_keep)
        self.keep_pid_button.clicked.connect(self.pid_keep)
        self.keep_kill_button.clicked.connect(self.kill_keep)

        self.command_layout.addWidget(self.adh_start_button, 0, 0)
        self.command_layout.addWidget(self.adh_stop_button, 0, 1)
        self.command_layout.addWidget(self.adh_restart_button, 0, 2)
        self.command_layout.addWidget(self.adh_status_button, 1, 0)
        self.command_layout.addWidget(self.adh_pid_button, 1, 1)
        self.command_layout.addWidget(self.adh_kill_button, 1, 2)

        self.command_layout.addWidget(self.keep_start_button, 2, 0)
        self.command_layout.addWidget(self.keep_stop_button, 2, 1)
        self.command_layout.addWidget(self.keep_restart_button, 2, 2)
        self.command_layout.addWidget(self.keep_status_button, 3, 0)
        self.command_layout.addWidget(self.keep_pid_button, 3, 1)
        self.command_layout.addWidget(self.keep_kill_button, 3, 2)

        # 设置输出区域
        self.output_text = QPlainTextEdit()
        self.output_text.setReadOnly(True)

        # 添加所有组件到主布局
        self.main_layout.addWidget(self.command_group)
        self.main_layout.addWidget(self.output_text)

        # 创建中心窗口并设置主布局
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # 设置菜单栏
        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)

        self.menu = QMenu("设置")
        self.menu_bar.addMenu(self.menu)

        self.setting_action = QAction("修改设置")
        self.menu.addAction(self.setting_action)
        self.setting_action.triggered.connect(self.open_config_dialog)

        # IP选择下拉框
        self.ip_selector = QComboBox(self)
        self.ip_selector.addItem("请选择IP")
        self.ip_selector.setMinimumWidth(150)  # Set a minimum width for the dropdown
        self.menu_bar.setCornerWidget(self.ip_selector)


        # 加载配置文件
        self.configs = {}
        self.load_config()

    def open_config_dialog(self):
        dialog = ConfigDialog(self)
        if dialog.exec_():
            ip, ok = QInputDialog.getText(self, "输入IP", "请输入IP地址:")
            if ok:
                self.configs[ip] = {
                    "user": dialog.ssh_user.text(),
                    "password": dialog.ssh_password.text(),
                    "path": dialog.adh_path.text(),
                }
                self.ip_selector.addItem(ip)
                self.save_config()

    def load_config(self):
        try:
            with open("DNS-Controller.conf", "r", encoding="utf-8") as f:
                self.configs = json.load(f)
                for ip in self.configs.keys():
                    self.ip_selector.addItem(ip)
        except FileNotFoundError:
            pass

    def save_config(self):
        with open("DNS-Controller.conf", "w", encoding="utf-8") as f:
            json.dump(self.configs, f)

    def execute_command(self, command):
        ip = self.ip_selector.currentText()
        if ip not in self.configs:
            self.output_text.appendPlainText("错误：未找到该IP的配置信息")
            return
        config = self.configs[ip]
        ssh = SSHClient(ip, config["user"], config["password"])
        result = ssh.execute(config["path"] + command)
        ssh.close()
        self.output_text.appendPlainText(result)

    # AdGuardHome commands
    def start_adh(self):
        self.execute_command("/AdGuardHome -s start")

    def stop_adh(self):
        self.execute_command("/AdGuardHome -s stop")

    def restart_adh(self):
        self.execute_command("/AdGuardHome -s restart")

    def status_adh(self):
        self.execute_command("/AdGuardHome -s status")

    def pid_adh(self):
        self.execute_command("pidof AdGuardHome")

    def kill_adh(self):
        self.execute_command("killall AdGuardHome") 

    # keepalived commands
    def start_keep(self):
        self.execute_command("service keepalived start")

    def stop_keep(self):
        self.execute_command("service keepalived stop")

    def restart_keep(self):
        self.execute_command("service keepalived restart")

    def status_keep(self):
        self.execute_command("service keepalived status")

    def pid_keep(self):
        self.execute_command("pidof keepalived")

    def kill_keep(self):
        self.execute_command("killall keepalived")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
