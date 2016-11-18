#!/usr/bin/python3.5
#Always run this with python3.5

import sys
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGraphicsBlurEffect, QGraphicsOpacityEffect, QGraphicsDropShadowEffect,
                             QGraphicsColorizeEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QColor

class Example(QGraphicsView):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.scene = QGraphicsScene()
        self.pixmap = QPixmap("geo5.jpg")
        self.font = QFont("PT Sans", 16)
        self.font.setBold(True)

        #self.scene.addPixmap(self.pixmap.scaled(300, 200))
        self.text = self.scene.addText("Praise to the Lord\nThe Almighty\nThe King of Creation", self.font)
        self.text.setDefaultTextColor(QColor(255, 255, 255))
        self.text.setFlags(QGraphicsItem.ItemIsSelectable |
                           QGraphicsItem.ItemIsMovable)
        self.text.setTextInteractionFlags(Qt.TextEditable)

        self.setScene(self.scene)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Graphics View')
        self.show()

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
        qp.drawPixmap(rect.toRect(), self.pixmap)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
