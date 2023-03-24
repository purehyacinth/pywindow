import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from untitled import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.setupUi(self)

        # 创建一个字典用来保存窗口的参数
        self.window={}
        self.i = 1
        # 按钮点击创建窗
        self.pushButton.clicked.connect(self.listwidget_add)
        self.pushButton_2.clicked.connect(self.listwidget_del)


        self.listWidget.itemClicked.connect(self.listwidget_click)
        self.listWidget.itemClicked.connect(self.plot)

        # 点击按钮修改窗口参数
        self.pushButton_3.clicked.connect(self.window_change)


    def create_window(self):
        # 类型和长度默认为 Hanning 和 64
        self.window_type="Hanning"
        self.window_length=64

        self.window[self.window_name]={'type':self.window_type,'length':self.window_length}
        print(self.window)

    def listwidget_add(self):

        self.listWidget.addItem('window_'+str(self.i))
        # 得到创建的窗口名字
        self.window_name='window_'+str(self.i)
        # 把窗口的参数保存到字典中
        self.create_window()
        self.i+=1

    def listwidget_del(self):
        # 获得删除的窗口名字，并且在字典中删除
        self.window_name = self.listWidget.currentItem().text()
        self.window.pop(self.window_name)
        self.listWidget.takeItem(self.listWidget.currentRow())

        # 删除后，把lineEdit和comboBox清空
        self.lineEdit.setText('')
        self.comboBox.setCurrentText('')
        self.lineEdit_3.setText('')

    def listwidget_click(self):
        self.window_name=self.listWidget.currentItem().text()

        # 选定窗口后，把窗口的参数显示在lineEdit中
        self.lineEdit.setText(self.window_name)
        # 将窗口类型显示到comboBox中
        self.comboBox.setCurrentText(self.window[self.window_name]['type'])
        # 显示长度
        self.lineEdit_3.setText(str(self.window[self.window_name]['length']))

    def window_change(self):
        # 获取lineEdit,comboBox,lineEdit_3的值,,并且更新到字典中
        self.window_name=self.lineEdit.text()
        self.window_type=self.comboBox.currentText()
        self.window_length=int(self.lineEdit_3.text())

        self.window[self.window_name]={'type':self.window_type,'length':self.window_length}
        # 更新listWidget的显示
        self.listWidget.currentItem().setText(self.window_name)

    def plot(self):
        pass

    def plot_deafault(self):
        self.fig1 = plt.figure()
        self.canvas1 = FigureCanvas(self.fig1)
        layout = QVBoxLayout()  # 垂直布局
        layout.addWidget(self.canvas1)
        self.graphicsView.setLayout(layout)  # 设置好布局之后调用函数

        self.fig2 = plt.figure()
        self.canvas2 = FigureCanvas(self.fig2)
        layout = QVBoxLayout()  # 垂直布局
        layout.addWidget(self.canvas2)
        self.fig2.subplots_adjust(left=None, bottom=0.2, right=None, top=None, wspace=None, hspace=None)
        self.ui.graphicsView_2.setLayout(layout)  # 设置好布局之后调用函数


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    # apply_stylesheet(app, theme='dark_blue.xml')
    mainWindow.show()
    sys.exit(app.exec_())