from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QWidget, QGraphicsItem, QMessageBox, QPushButton, QFileDialog
from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtGui import QPen, QPainterPath, QPixmap
from PIL import Image
import numpy as np
import sys

class LineItem(QGraphicsItem):
    def __init__(self, start_point, end_point):
        super().__init__()
        self.start_point = start_point
        self.end_point = end_point

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

class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.scene_pos_A = 0
        self.record_A = False
        self.scene_pos_B = 0
        self.record_B = False
        self.line_item = 0
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            scene_pos = self.mapToScene(event.pos())
            if self.record_A:
                self.scene_pos_A = scene_pos
                self.show(scene_pos)
                self.record_A = False
            elif self.record_B:
                self.scene_pos_B = scene_pos
                self.show(scene_pos)
                self.record_B = False
            if self.scene_pos_A and self.scene_pos_B:
                self.line_item = LineItem(self.scene_pos_A, self.scene_pos_B)
                self.scene().addItem(self.line_item)
        super().mousePressEvent(event)

    def show(self, scene_pos):
        mbox = QMessageBox()
        mbox.information(self, 'Success!', f"record\nX:{scene_pos.x()}\nY:{scene_pos.y()}")
        pass

class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.img_path = ""
        
        self.setObjectName("Form")
        self.resize(600, 750)
        self.graphicsView = CustomGraphicsView(self)
        self.graphicsView.setGeometry(QRect(0, 0, 500, 500))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView_2 = CustomGraphicsView(self)
        self.graphicsView_2.setGeometry(QRect(0, 600, 580, 150))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QRect(520, 50, 60, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setGeometry(QRect(520, 100, 60, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QPushButton(self)
        self.pushButton_3.setGeometry(QRect(520, 150, 60, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QPushButton(self)
        self.pushButton_4.setGeometry(QRect(520, 200, 60, 25))
        self.pushButton_4.setObjectName("pushButton_5")
        self.pushButton_5 = QPushButton(self)
        self.pushButton_5.setGeometry(QRect(520, 250, 60, 25))
        self.pushButton_5.setObjectName("pushButton_5")

        self.retranslateUi()
        self.pushButton.clicked.connect(self.choose_img)
        self.pushButton_2.clicked.connect(self.set_A)
        self.pushButton_3.clicked.connect(self.set_B)
        self.pushButton_4.clicked.connect(self.calculate)
        self.pushButton_5.clicked.connect(self.clear)
        
    def retranslateUi(self):
        self.setWindowTitle("Form")
        self.pushButton.setText("Image")
        self.pushButton_2.setText("penA")
        self.pushButton_3.setText("penB")
        self.pushButton_4.setText("Cal")
        self.pushButton_5.setText("Clear")

    def choose_img(self):
        try:
            img_path, filterType = QFileDialog.getOpenFileNames()
            self.img_path = img_path[0]
            scene = QGraphicsScene()
            scene.addPixmap(QPixmap(self.img_path).scaled(450, 450))        
            self.graphicsView.setScene(scene)
        except:
            pass

    def set_A(self):
        self.graphicsView.record_A = True
        pass

    def set_B(self):
        self.graphicsView.record_B = True
        pass

    def calculate(self):
        img = Image.open(self.img_path).resize((450, 450))
        img_arr = np.array(img)
        line = [(self.graphicsView.scene_pos_A.x(), self.graphicsView.scene_pos_A.y()), (self.graphicsView.scene_pos_B.x(), self.graphicsView.scene_pos_B.y())]

        x_world, y_world = zip(*line)
        x_world = np.array(x_world)
        y_world = np.array(y_world)
        print(x_world)
        pass

    def clear(self):
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap(self.img_path).scaled(450, 450))        
        self.graphicsView.setScene(scene)
        self.graphicsView.scene_pos_A = 0
        self.graphicsView.scene_pos_B = 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    sys.exit(app.exec_())
