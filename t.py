import sys
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsItem
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QPainterPath


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


class MyGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.initUI()
        self.x = 10
        self.y = 10

    def initUI(self):
        # 创建一个线条项并添加到场景中
        self.line_item = LineItem(QPointF(0, 0), QPointF(100, 100))
        self.scene.addItem(self.line_item)

    def moveLine(self, dx, dy):
        # 移动线条的起点和终点
        self.scene.removeItem(self.line_item)
        new_start_point = self.line_item.start_point + QPointF(dx, dy)
        new_end_point = self.line_item.end_point + QPointF(dx, dy)
        self.line_item.start_point = new_start_point
        self.line_item.end_point = new_end_point
        self.scene.addItem(self.line_item)

    def mousePressEvent(self, event):
        self.moveLine(self.x, self.y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = MyGraphicsView()
    view.show()

    # 移动线条的示例
    view.moveLine(50, 50)

    sys.exit(app.exec_())
