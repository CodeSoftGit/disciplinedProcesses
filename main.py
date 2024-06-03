import ctypes
import sys
import os
import winreg as reg
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QRadioButton, QButtonGroup, QMessageBox
from qfluentwidgets import CaptionLabel, setTheme, Theme, RadioButton, PrimaryPushButton

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([script] + sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

def set_cpu_priority(executable_name, priority_value):
    try:
        reg_path = f"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\{executable_name}\\PerfOptions"
        reg_key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, reg_path)
        reg.SetValueEx(reg_key, "CpuPriorityClass", 0, reg.REG_DWORD, priority_value)
        reg.CloseKey(reg_key)
        QMessageBox.information(None, "Success", f"CpuPriorityClass set to {priority_value} for {executable_name}")
    except Exception as e:
        QMessageBox.critical(None, "Error", f"An error occurred: {e}")

class Demo(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Set CPU Priority Class")
        self.setGeometry(100, 100, 400, 300)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.vBoxLayout.setSpacing(20)

        self.executableLabel = CaptionLabel("Enter the executable name:", self)
        self.vBoxLayout.addWidget(self.executableLabel)
        
        self.executableEntry = QLineEdit(self)
        self.vBoxLayout.addWidget(self.executableEntry)

        self.priorityLabel = CaptionLabel("Choose the CPU priority class:", self)
        self.vBoxLayout.addWidget(self.priorityLabel)

        self.buttonGroup = QButtonGroup(self)

        self.radioHigh = RadioButton("High: 00000003", self)
        self.radioHigh.setChecked(True)
        self.buttonGroup.addButton(self.radioHigh, 0x00000003)
        self.vBoxLayout.addWidget(self.radioHigh)

        self.radioAboveNormal = RadioButton("Above Normal: 00000006", self)
        self.buttonGroup.addButton(self.radioAboveNormal, 0x00000006)
        self.vBoxLayout.addWidget(self.radioAboveNormal)

        self.radioNormal = RadioButton("Normal: 00000002", self)
        self.buttonGroup.addButton(self.radioNormal, 0x00000002)
        self.vBoxLayout.addWidget(self.radioNormal)

        self.radioBelowNormal = RadioButton("Below Normal: 00000005", self)
        self.buttonGroup.addButton(self.radioBelowNormal, 0x00000005)
        self.vBoxLayout.addWidget(self.radioBelowNormal)

        self.radioLow = RadioButton("Low: 00000001", self)
        self.buttonGroup.addButton(self.radioLow, 0x00000001)
        self.vBoxLayout.addWidget(self.radioLow)

        self.setPriorityButton = PrimaryPushButton("Set Priority", self)
        self.setPriorityButton.clicked.connect(self.on_submit)
        self.vBoxLayout.addWidget(self.setPriorityButton)

    def on_submit(self):
        executable_name = self.executableEntry.text()
        priority_value = self.buttonGroup.checkedId()

        if not executable_name:
            QMessageBox.critical(self, "Error", "Please enter the executable name.")
            return

        set_cpu_priority(executable_name, priority_value)

if __name__ == '__main__':
    if not is_admin():
        run_as_admin()
        sys.exit(0)

    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    setTheme(Theme.LIGHT)  # Set theme to light, change to Theme.DARK if you prefer dark theme

    window = Demo()
    window.show()

    sys.exit(app.exec_())
