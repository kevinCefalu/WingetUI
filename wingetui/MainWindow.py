from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import Tabs, os, ctypes, sys, Tools

if hasattr(sys, 'frozen'):
    realpath = sys._MEIPASS
else:
    realpath = '/'.join(sys.argv[0].replace("\\", "/").split("/")[:-1])

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("WingetUI Store: A GUI Store for Winget and Scoop packages")
        self.setMinimumSize(700, 560)
        self.setObjectName("micawin")
        self.setWindowIcon(QtGui.QIcon(realpath+"/icon.png"))
        self.resize(QtCore.QSize(1100, 700))
        self.loadWidgets()
        self.installEventFilter(self)
        self.show()
        self.setStyleSheet("""
            QTreeWidget::item{{
                height: 25px;
                padding: 5px;
                padding-left: 10px;
            }}
            QGroupBox:title{{ max-width: 0; max-height: 0; }}
        """)

        if(self.isAdmin()):
            QtWidgets.QMessageBox.warning(self, "Admin rights", "It looks like you have ran this software with admin rights. We do not recommend doing this. Proceed with caution")
        print("[   OK   ] Main application loaded...")

    def loadWidgets(self) -> None:
        self.mainWidget = QtWidgets.QStackedWidget()
        self.buttonBox = QButtonGroup()
        self.buttonLayout = QHBoxLayout()
        self.mainWidget.setStyleSheet("""
        QTabWidget::tab-bar {{
            alignment: center;
            }}""")
        self.discover = Tabs.Discover()
        self.discover.setStyleSheet("QGroupBox{border-radius: 5px;}")
        self.buttonLayout.addWidget(QWidget(), stretch=1)
        self.addTab(self.discover, "Discover Software")
        self.addTab(Tabs.Uninstall(), "Installed applications")
        self.addTab(Tabs.About(), "About WingetUI")
        self.buttonLayout.addWidget(QWidget(), stretch=1)
        vl = QVBoxLayout()
        vl.addLayout(self.buttonLayout, stretch=0)
        vl.addWidget(self.mainWidget, stretch=1)
        vl.setContentsMargins(0, 20, 0, 0)
        w = QWidget()
        w.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        w.setLayout(vl)
        self.setCentralWidget(w)
        self.show()
        self.discover.resizeEvent()

    def addTab(self, widget: QWidget, label: str) -> None:
        i = self.mainWidget.addWidget(widget)
        btn = QPushButton(label)
        btn.setCheckable(True)
        btn.clicked.connect(lambda: self.mainWidget.setCurrentIndex(i))
        self.buttonBox.addButton(btn)
        self.buttonLayout.addWidget(btn)

    def isAdmin(self) -> bool:
        try:
            is_admin = (os.getuid() == 0)
        except AttributeError:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        return is_admin
    
    def closeEvent(self, event):
        if(Tools.pending_programs != []):
            if(QtWidgets.QMessageBox.question(self, "Warning", "There is an installation in progress. If you close WingetUI Store, the installation may fail and have unexpected results. Do you still want to close the application?", QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes):
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


if(__name__=="__main__"):
    import __init__
