import sys

import numpy as np
from PyQt5.QtCore import QRectF, Qt, QPoint
from PyQt5.QtGui import QContextMenuEvent, QTransform
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsEllipseItem, QVBoxLayout, QMenu, \
    QGraphicsView
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from test_scene import Ui_MainWindow

class TestScene(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(TestScene, self).__init__()
        self.setupUi(self)

        self.scene = QGraphicsScene()

        self.graphicsView.setScene(self.scene)
        self.scene.setSceneRect(0, 0, self.graphicsView.width(), self.graphicsView.height())

        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.graphicsView.mousePressEvent = self.on_mouse_press_event

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.scene.addWidget(self.canvas)

        self.pushButton.clicked.connect(self.plot)

        self.item=[]

    def on_mouse_press_event(self, event):
        # 判断是否为右键按下
        if event.button() == Qt.RightButton:
            # 找到最近的点并删除
            nearest_item = self.scene.itemAt(self.graphicsView.mapToScene(event.pos()), QTransform())
            if nearest_item and isinstance(nearest_item, QGraphicsEllipseItem):
                self.scene.removeItem(nearest_item)
        else:
            # 获取鼠标点击的位置
            pos = event.pos()
            print(pos)

            print(self.line)




            # 创建一个圆形图形项
            # circle_item = QGraphicsEllipseItem(QRectF(-10, -10, 20, 20))
            # circle_item.setPos(pos.x(), pos.y())
            # circle_item.setBrush(Qt.red)
            # # 将圆形图形项添加到场景中
            # self.scene.addItem(circle_item)

    def plot(self):
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        plt.plot(x, y)

        self.line=plt.plot(x, y,picker=50)

        self.canvas.draw()
        self.scene.setSceneRect(0, 0, self.graphicsView.width(), self.graphicsView.height())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setStyle('Fusion')
    mainWindow = TestScene()
    mainWindow.show()
    sys.exit(app.exec_())