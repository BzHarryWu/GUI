import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QSlider, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPointF, QRectF, QLineF
from PyQt5.QtGui import QPainter, QPen, QColor, QTransform, QPainterPath

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("360度線條投射")
        self.setGeometry(100, 100, 600, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 360)  # 设置滑动范围为0到360度
        layout.addWidget(self.slider)

        self.slider.valueChanged.connect(self.update_line)

        self.update_line(0)

    def update_line(self, angle):
        self.scene.clear()

        pen = QPen(QColor("blue"))
        pen.setWidth(2)
        self.scene.addLine(0, 0, 100, 0, pen)

        transform = QTransform()
        transform.rotate(angle)
        rotated_line = transform.map(QLineF(0, 0, 100, 0))

        self.scene.addLine(rotated_line, pen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
