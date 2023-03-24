import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 创建一个菜单栏
        menubar = self.menuBar()

        # 创建一个文件菜单
        fileMenu = menubar.addMenu('文件')

        # 创建一个动作
        newAct = QAction('新建', self)
        newAct.setShortcut('Ctrl+N')
        newAct.setStatusTip('创建新文件')
        newAct.triggered.connect(self.newFile)

        # 将动作添加到文件菜单中
        fileMenu.addAction(newAct)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('打开新窗口')
        self.show()

    def newFile(self):
        # 创建一个新窗口
        new_window = QWidget()
        new_window.setGeometry(100, 100, 200, 150)
        new_window.setWindowTitle('新窗口')
        new_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
