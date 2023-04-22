import matplotlib.backends.backend_qt5agg as mpl_backend
from PyQt5 import QtWidgets

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # 初始化 Matplotlib 和 QGraphicsScene
        self.figure = mpl_backend.FigureCanvasQTAgg(self).figure
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene)

        # 在 Figure 上绘制一条线
        axes = self.figure.add_subplot(111)
        axes.plot([0, 1, 2], [0, 1, 2])

        # 将 Figure 嵌入到 QGraphicsScene 中
        self.scene.addWidget(self.figure.canvas)

        # 显示 QGraphicsView
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)

    def mousePressEvent(self, event):
        # 获取鼠标点击的位置
        view_pos = event.pos()
        scene_pos = self.view.mapToScene(view_pos)

        # 将点击位置从 QGraphicsScene 的坐标系转换到 Matplotlib 的坐标系
        renderer = self.figure.canvas.get_renderer()
        bbox = self.figure.bbox_inches.transformed(renderer.dpi_scale_trans.inverted())
        mpl_pos = (
            (scene_pos.x() - bbox.x0) / bbox.width,
            1 - (scene_pos.y() - bbox.y0) / bbox.height
        )

        # 输出坐标信息
        print("View pos:", view_pos)
        print("Scene pos:", scene_pos)
        print("Matplotlib pos:", mpl_pos)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
