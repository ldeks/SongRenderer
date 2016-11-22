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
        self.shadowSize = 5
        self.shadowRatio = self.shadowSize/float(16)
        self.shadowOffset = 2
        self.shadowOffsetRatio = self.shadowOffset/float(16)

        self.text = self.scene.addText("Praise to the Lord\nThe Almighty\nThe King of Creation", self.font)
        self.text.setDefaultTextColor(QColor(255, 255, 255))
        self.text.setFlags(QGraphicsItem.ItemIsSelectable |
                           QGraphicsItem.ItemIsMovable)

        self.setScene(self.scene)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Graphics View')
        self.show()

    def resizeEvent(self, e):
        self.adjustText()
        self.scene.setSceneRect(QRectF(self.viewport().rect()))
        self.centerText()

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Up:
            self.rotate(30)

        elif e.key() == Qt.Key_Down:
            self.rotate(-30)

        elif e.key() == Qt.Key_B:

            shadow = QGraphicsBlurEffect()
            shadow.setBlurRadius(self.shadowSize)
            self.text.setGraphicsEffect(shadow)

        elif e.key() == Qt.Key_S:

            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(self.shadowSize)
            shadow.setOffset(self.shadowOffset)
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
        scaleFactor = 0.65
        fontSize = self.text.font().pointSize() * scaleFactor * fontRatio
        self.font.setPointSizeF(fontSize)
        self.shadowSize = int(fontSize * self.shadowRatio)
        self.shadowOffset = int(scaleFactor * fontSize * self.shadowOffsetRatio)
        self.text.setFont(self.font)

        # Must do duck typing here because the object takes ownership
        # of its graphics effect object and deletes it when it's changed.
        try:
            self.text.graphicsEffect().setBlurRadius(self.shadowSize)
            self.text.graphicsEffect().setOffset(self.shadowOffset)
            self.text.graphicsEffect().update()
        except(AttributeError, TypeError):
            pass

    def centerText(self):

        # The center of the text block
        rect = self.text.boundingRect()
        rectCenter = QPointF(rect.width()/2, rect.height()/2)

        # The center of the window
        windowWidth = self.viewport().width()
        windowHeight = self.viewport().height()
        centerPos = QPointF(float(windowWidth)/2, float(windowHeight)/2)

        # The desired new location
        topLeftPos = centerPos - QPointF(rect.width()/2, rect.height()/2)

        # Any position of the text relative to the scene
        rectS = self.text.mapRectToScene(rect)

        # Move the text to the center position
        self.text.moveBy(topLeftPos.x()-rectS.x(), topLeftPos.y()-rectS.y())



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
