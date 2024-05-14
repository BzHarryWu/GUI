from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QWidget, QGraphicsItem, QMessageBox
from PyQt6.QtCore import Qt, QRect
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPen, QPainterPath
from PIL import Image
import numpy as np

class LineItem(QGraphicsItem):
    def __init__(self, start_point, end_point):
        super().__init__()
        self.start_point = start_point
        self.end_point = end_point

    def boundingRect(self):
        # Return the bounding rectangle of the line
        return self.shape().boundingRect()

    def shape(self):
        # Define the shape of the line for interaction purposes
        path = QPainterPath()
        path.moveTo(self.start_point)
        path.lineTo(self.end_point)
        return path

    def paint(self, painter, option, widget):
        # Paint method to draw the line
        painter.setPen(QPen(Qt.GlobalColor.red))
        painter.drawLine(self.start_point, self.end_point)

class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.scene_pos_A = 0
        self.record_A = False
        self.scene_pos_B = 0
        self.record_B = False
        self.line_item = 0
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            scene_pos = self.mapToScene(event.position().toPoint())
        super().mousePressEvent(event)
        if self.record_A:
            self.scene_pos_A = scene_pos
            self.show(scene_pos)
        elif self.record_B:
            self.scene_pos_B = scene_pos
            self.show(scene_pos)
        self.record_A = False
        self.record_B = False
        if self.scene_pos_A and self.scene_pos_B:
            self.line_item = LineItem(self.scene_pos_A, self.scene_pos_B)
            self.scene().addItem(self.line_item)

    def show(self, scene_pos):
        mbox = QMessageBox(self)
        mbox.information(self, 'Success!', f"record\nX:{scene_pos.x()}\nY:{scene_pos.y()}")
        pass

class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.img_path = ""
        
        self.setObjectName("Form")
        self.resize(574, 742)
        self.graphicsView = CustomGraphicsView(self)
        self.graphicsView.setGeometry(QRect(0, 0, 500, 500))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView_2 = CustomGraphicsView(self)
        self.graphicsView_2.setGeometry(QRect(0, 581, 571, 161))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QRect(510, 50, 56, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QRect(510, 100, 56, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QRect(510, 150, 56, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QRect(510, 200, 56, 25))
        self.pushButton_4.setObjectName("pushButton_5")
        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.setGeometry(QRect(510, 250, 56, 25))
        self.pushButton_5.setObjectName("pushButton_5")

        self.retranslateUi()
        self.pushButton.clicked.connect(self.choose_img)
        self.pushButton_2.clicked.connect(self.set_A)
        self.pushButton_3.clicked.connect(self.set_B)
        self.pushButton_4.clicked.connect(self.calculate)
        self.pushButton_5.clicked.connect(self.clear)
        
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText(_translate("Form", "Image"))
        self.pushButton_2.setText(_translate("Form", "penA"))
        self.pushButton_3.setText(_translate("Form", "penB"))
        self.pushButton_4.setText(_translate("Form", "Cal"))
        self.pushButton_5.setText(_translate("Form", "Clear"))

    def choose_img(self):
        try:
            img_path, filterType = QtWidgets.QFileDialog.getOpenFileNames()
            self.img_path = img_path[0]
            scene = QtWidgets.QGraphicsScene()
            scene.addPixmap(QtGui.QPixmap(self.img_path).scaled(500,500))        
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
        img = Image.open(self.img_path).resize((500,500))
        img_arr = np.array(img)
        line = [(self.graphicsView.scene_pos_A.x(), self.graphicsView.scene_pos_A.y()), (self.graphicsView.scene_pos_B.x(), self.graphicsView.scene_pos_B.y())]

        x_world, y_world = zip(*line)
        x_world = np.array(x_world)
        y_world = np.array(y_world)
        print(x_world)
        pass

    def clear(self):
        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(QtGui.QPixmap(self.img_path).scaled(500,500))        
        self.graphicsView.setScene(scene)
        self.graphicsView.scene_pos_A = 0
        self.graphicsView.scene_pos_B = 0

if __name__ == "__main__":
    app = QApplication([])
    form = MainForm()
    form.show()
    app.exec()

#https://stackoverflow.com/questions/18920614/plot-cross-section-through-heat-map