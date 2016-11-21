#!/usr/bin/python3.5
#Always run this with python3.5

import sys
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGraphicsBlurEffect, QGraphicsOpacityEffect, QGraphicsDropShadowEffect,
                             QGraphicsColorizeEffect)
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPixmap, QFont, QColor, QMatrix4x4

class Example(QGraphicsView):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.scene = QGraphicsScene()
        self.pixmap = QPixmap("geo5.jpg")
        self.font = QFont("PT Sans", 16)
        self.font.setBold(True)

        self.text = self.scene.addText("Praise to the Lord\nThe Almighty\nThe King of Creation", self.font)
        self.text.setDefaultTextColor(QColor(255, 255, 255))
        self.text.setFlags(QGraphicsItem.ItemIsSelectable |
                           QGraphicsItem.ItemIsMovable)
        self.adjustText()

        self.setScene(self.scene)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Graphics View')
        self.show()

    def resizeEvent(self, e):
        super(Example, self).resizeEvent(e)
        self.adjustText()

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Up:
            self.rotate(30)

        elif e.key() == Qt.Key_Down:
            self.rotate(-30)

        elif e.key() == Qt.Key_B:

            self.text.setGraphicsEffect(QGraphicsBlurEffect())

        elif e.key() == Qt.Key_S:

            shadow = QGraphicsDropShadowEffect()
            shadow.setOffset(2)
            shadow.setBlurRadius(5)
            self.text.setGraphicsEffect(shadow)

        elif e.key() == Qt.Key_C:

            self.text.setGraphicsEffect(QGraphicsColorizeEffect())

        elif e.key() == Qt.Key_O:

            self.text.setGraphicsEffect(QGraphicsOpacityEffect())

        elif e.key() == Qt.Key_N:
                self.text.setGraphicsEffect(None)

    def drawBackground(self, qp, rect):

        # The rectangle is in "Scene coordinates".  mapFromScene converts to viewport coordinates
        # Not sure how scene coordinates and self.sceneRect() relate.
        # The QGraphicsView source code shows the how the rectangle is computed and passed in.
        viewRect = QRectF(self.mapFromScene(rect).boundingRect())

        # Need to scale the rectangle from viewport coordinates to pixmap coordinates
        # This is matrix algebra.
        scaleMatrix = QMatrix4x4()
        scaleMatrix.scale(float(self.pixmap.width())/self.viewport().width(),
                          float(self.pixmap.height())/self.viewport().height())
        pixmapRect = scaleMatrix.mapRect(viewRect)

        # Now we have the target drawing buffer (rect in scene coordinates)
        # as well as the source drawing buffer (rect in pixmap coordinates).
        # We are sampling correctly from both.
        qp.drawPixmap(rect, self.pixmap, pixmapRect)

    def adjustText(self):

        fontRatio = float(self.viewport().width())/(self.text.boundingRect().width())
        scaleFactor = 0.75
        fontSize = self.text.font().pointSize() * scaleFactor * fontRatio
        self.font.setPointSizeF(fontSize)
        self.text.setFont(self.font)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
