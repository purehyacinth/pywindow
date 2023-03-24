import sys

import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from qtpy import uic

from untitled import Ui_MainWindow
from new_untitled import Ui_Form
from scipy.signal import get_window

class Widget(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.ui=Ui_Form()
        self.setupUi(self)

        self.lineEdit.setText('512')
        self.comboBox.setCurrentIndex(0)
class MainWindow(QMainWindow, Ui_MainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.setupUi(self)

        # 实例化一个widget
        self.widget=Widget()
        # 点击analyse_parameter按钮，弹出widget
        self.actionAnalyse_Parameter.triggered.connect(self.widget.show)

        # 点击widget在中的apply按钮，将参数传递到主窗口
        self.widget.pushButton.clicked.connect(self.apply)

        # 创建一个字典用来保存窗口的参数
        self.window={}
        self.i = 1
        self.plot_deafault()
        self.point_num=512
        self.combo_index=0
        self.lineEdit_2.setEnabled(False)
        # 按钮点击创建窗
        self.pushButton.clicked.connect(self.listwidget_add)
        self.pushButton_2.clicked.connect(self.listwidget_del)

        self.listWidget.itemClicked.connect(self.listwidget_click)
        self.listWidget.itemClicked.connect(self.plot)

        # 点击按钮修改窗口参数
        self.pushButton_3.clicked.connect(self.window_change)

        # 让菜单栏的选项设为可勾选状态，并默认被勾选
        self.actionTime_Domain.setCheckable(True)
        self.actionFrequency_Domain_2.setCheckable(True)

        self.actionTime_Domain.setChecked(True)
        self.actionFrequency_Domain_2.setChecked(True)

        # 点击菜单栏的选项，显示或者隐藏对应的图像
        self.actionTime_Domain.triggered.connect(self.show_time)
        self.actionFrequency_Domain_2.triggered.connect(self.show_freq)

        # 点击复制按钮复制一个窗
        self.pushButton_4.clicked.connect(self.copy_window)

        # combo选中窗Kaiser后，lineEdit_2可用
        self.comboBox.currentIndexChanged.connect(self.setting_enable)
    def setting_enable(self):
        if self.comboBox.currentIndex()==4:
            self.lineEdit_2.setEnabled(True)
            self.label_4.setText('beta')
        else:
            self.lineEdit_2.setEnabled(False)
            self.lineEdit_4.setEnabled(False)
            self.label_4.setText('Parameter')
    def apply(self):
        # 获取点数
        self.point_num = int(self.widget.lineEdit.text())
        # 获取combo选择了第几个
        self.combo_index = self.widget.comboBox.currentIndex()
        # 刷新图像(仅在选中窗口的情况下)
        if self.listWidget.currentItem():
            self.plot()

    def show_time(self):
        if self.actionTime_Domain.isChecked():
            self.graphicsView.show()
        else:
            self.graphicsView.hide()
    def show_freq(self):
        if self.actionFrequency_Domain_2.isChecked():
            self.graphicsView_2.show()
        else:
            self.graphicsView_2.hide()

    def create_window(self):
        # 类型和长度默认为 Hanning 和 64
        self.window_type='hann'
        self.window_length=64

        self.window[self.window_name]={'type':self.window_type,'length':self.window_length}

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
        # 当parameter可用时，一定要填入参数
        if self.lineEdit_2.isEnabled():
            try:
                number=float(self.lineEdit_2.text())
            except:
                QMessageBox.warning(self, 'Warning', 'Please input number!', QMessageBox.Yes)
                return
        # 检测是否为数字参数，否则弹出窗口警告
        if self.lineEdit.text()!='' and self.lineEdit_3.text().isdigit():
            # 获取lineEdit,comboBox,lineEdit_3的值,,并且更新到字典中
            self.window_name=self.lineEdit.text()
            self.window_type=self.comboBox.currentText()
            self.window_length=int(self.lineEdit_3.text())
            self.window[self.window_name]={'type':self.window_type,'length':self.window_length}
            # 更新listWidget的显示
            self.listWidget.currentItem().setText(self.window_name)
            # 更新图像
            self.plot()
        else:
            QMessageBox.warning(self, 'Warning', 'Please input number!', QMessageBox.Yes)
    def plot(self):
        # 获取窗口的类型,如果是Kaiser，获取beta
        if self.comboBox.currentIndex()==4:
            window=get_window((self.window[self.window_name]['type'],float(self.lineEdit_2.text())),int(self.window[self.window_name]['length']))
        else:
            window=get_window(self.window[self.window_name]['type'],int(self.window[self.window_name]['length']))

        t=np.arange(self.window[self.window_name]['length'])
        # 计算频域

        freqs = np.arange(self.point_num) / self.point_num * 2 * np.pi
        fft_vals = np.abs(np.fft.fft(window, self.point_num)[:self.point_num])
        freqs_normalized = freqs / np.pi



        # 绘制时域图像
        self.canvas1.figure.clf()
        ax1 = self.canvas1.figure.add_subplot(111)
        ax1.grid(True)
        ax1.plot(t, window)
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Amplitude')
        ax1.set_title('Time Domain')
        self.canvas1.draw()
        # 绘制频域图像
        self.canvas2.figure.clf()
        ax2=self.canvas2.figure.add_subplot(111)
        ax2.plot(freqs_normalized, 20*np.log10(fft_vals + 1e-15),color='b')
        # 画出负半轴对称图形
        ax2.plot(-freqs_normalized, 20*np.log10(fft_vals + 1e-15),color='b')


        if self.combo_index==0:
            ax2.set_xlim([0, 1])
        elif self.combo_index==1:
            ax2.set_xlim([0, 2])
        elif self.combo_index==2:
            ax2.set_xlim([-1, 1])
        ax2.set_ylim([-150, 50])
        ax2.grid(True)
        ax2.set_xlabel('Frequency')
        ax2.set_ylabel('Magnitude(dB)')
        ax2.set_title('Frequency Domain')
        self.canvas2.draw()

    def plot_deafault(self):
        self.fig1 = plt.figure()
        self.canvas1 = FigureCanvas(self.fig1)
        layout = QVBoxLayout()  # 垂直布局
        layout.addWidget(self.canvas1)
        self.fig1.subplots_adjust(left=0.2, bottom=None, right=0.9, top=None, wspace=None, hspace=None)
        self.graphicsView.setLayout(layout)  # 设置好布局之后调用函数

        self.fig2 = plt.figure()
        self.canvas2 = FigureCanvas(self.fig2)
        layout = QVBoxLayout()  # 垂直布局
        layout.addWidget(self.canvas2)
        self.graphicsView_2.setLayout(layout)  # 设置好布局之后调用函数

    def copy_window(self):
        if self.listWidget.currentItem():
            self.window[self.window_name+'_copy']={'type':self.window[self.window_name]['type'],'length':self.window[self.window_name]['length']}
            self.listWidget.addItem(self.window_name+'_copy')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    # apply_stylesheet(app, theme='dark_blue.xml')
    mainWindow.show()
    sys.exit(app.exec_())