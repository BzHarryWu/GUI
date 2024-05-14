import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPen, QPainterPath
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt

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


class MyGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene())
        self.setSceneRect(0, 0, 400, 400)

        start_point = QPointF(50, 50)
        end_point = QPointF(200, 200)
        line_item = LineItem(start_point, end_point)
        self.scene().addItem(line_item)


if __name__ == "__main__":
    x, y = np.mgrid[-5:5:0.1, -5:5:0.1]
    z = np.sqrt(x**2 + y**2) + np.sin(x**2 + y**2)
    print(z)
    print(type(z))
    print(z.shape)

    line = [(-3, -1), (4, 3)]

    # Convert the line to pixel/index coordinates
    x_world, y_world = np.array(list(zip(*line)))
    col = z.shape[1] * (x_world - x.min()) / x.ptp()
    row = z.shape[0] * (y_world - y.min()) / y.ptp()

    # Interpolate the line at "num" points...
    num = 1000
    row, col = [np.linspace(item[0], item[1], num) for item in [row, col]]

    # Extract the values along the line, using cubic interpolation
    zi = scipy.ndimage.map_coordinates(z, np.vstack((row, col)))

    # Plot...
    fig, axes = plt.subplots(nrows=2)
    axes[0].pcolormesh(x, y, z)
    axes[0].plot(x_world, y_world, 'ro-')
    axes[0].axis('image')

    axes[1].plot(zi)

    plt.show()