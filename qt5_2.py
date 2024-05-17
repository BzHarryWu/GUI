from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QWidget, QGraphicsItem, QMessageBox, QPushButton, QFileDialog, QSlider
from PyQt5.QtCore import Qt, QRect, pyqtSignal, QPointF, QLineF
from PyQt5.QtGui import QPen, QPainterPath, QPixmap, QTransform
from PIL import Image
import numpy as np
import sys
import math

class LineItem(QGraphicsItem):
    def __init__(self, start_point, end_point):
        super().__init__()
        self.start_point = QPointF(*start_point)
        self.end_point = QPointF(*end_point)
        self.angle = 0

    def boundingRect(self):
        return self.shape().boundingRect()

    def shape(self):
        path = QPainterPath()
        path.moveTo(self.start_point)
        path.lineTo(self.end_point)
        return path

    def paint(self, painter, option, widget):
        pen = QPen(Qt.red)
        pen.setWidth(2)  # 根据需要调整线条的宽度
        painter.setPen(pen)
        painter.drawLine(self.start_point, self.end_point)

class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.img_path = ""
        self.slide_val = 0
        self.pic_scene = QGraphicsScene()
        self.line_item = LineItem((0 , 250), (500 ,250))


        self.setObjectName("Form")
        self.resize(600, 750)
        self.graphicsView = QGraphicsView(self)
        self.graphicsView.setGeometry(QRect(0, 0, 500, 500))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView_2 = QGraphicsView(self)
        self.graphicsView_2.setGeometry(QRect(0, 600, 550, 150))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QRect(520, 50, 60, 50))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_4 = QPushButton(self)
        self.pushButton_4.setGeometry(QRect(520, 250, 60, 50))
        self.pushButton_4.setObjectName("pushButton_5")
        self.slide_1 = QSlider(self)
        self.slide_1.setOrientation(1)
        self.slide_1.setGeometry(QRect(50, 550, 400, 20))
        self.slide_1.setRange(0,180)

        self.retranslateUi()
        self.pushButton.clicked.connect(self.choose_img)
        self.pushButton_4.clicked.connect(self.calculate)
        self.slide_1.valueChanged.connect(self.slide_change)
        
    def retranslateUi(self):
        self.setWindowTitle("Form")
        self.pushButton.setText("Image")
        self.pushButton_4.setText("Cal")

    def choose_img(self):
        try:
            img_path, filterType = QFileDialog.getOpenFileNames()
            self.img_path = img_path[0]
            self.pic_scene.addPixmap(QPixmap(self.img_path).scaled(500, 500))        
            self.graphicsView.setScene(self.pic_scene)
            self.graphicsView.fitInView(self.pic_scene.sceneRect(), Qt.KeepAspectRatio)
            self.graphicsView.scene().addItem(self.line_item)
            self.slide_1.setValue(0)
        except:
            pass

    def calculate(self):
        img = Image.open(self.img_path).resize((500, 500)).convert('L')
        img_arr = np.array(img)

        pass

    def slide_change(self, angle):
        self.pic_scene.removeItem(self.line_item)
        pointA = ((250 + 250 * math.cos(math.radians(angle))), (250 + 250 * math.sin(math.radians(angle))))
        pointB = ((250 - 250 * math.cos(math.radians(angle))), (250 - 250 * math.sin(math.radians(angle))))
        self.line_item.start_point = QPointF(*pointA)
        self.line_item.end_point = QPointF(*pointB)
        self.pic_scene.addItem(self.line_item)
        
        
if __name__ == "__main__":

    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    sys.exit(app.exec_())
