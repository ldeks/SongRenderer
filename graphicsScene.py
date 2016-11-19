#!/usr/bin/python3.5
#Always run this with python3.5

import sys
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGraphicsBlurEffect, QGraphicsOpacityEffect, QGraphicsDropShadowEffect,
                             QGraphicsColorizeEffect)
from PyQt5.QtCore import Qt, QRectF, QPointF
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
        #self.text.setTextInteractionFlags(Qt.TextEditable)
        self.bkgOriginX = None
        self.bkgOriginY = None

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
        #if not self.backgroundRect:
        #    self.backgroundRect.append(rect.toRect())
        ##print(self.sceneRect(), end = ' ')
        ##print(self.pixmap.rect())
        #print(qp.device().width(), qp.device().height())

        #target = rect
        #offset = QPointF(self.pixmap.width() / 2.0, self.pixmap.height() / 2.0)
        ##offset = QPointF(502, 242)
        #print(offset)
        #source = QRectF(rect.topLeft() + offset, rect.size())
        #qp.drawPixmap(target, self.pixmap, source)
        #qp.drawPixmap(0, 0, self.width(), self.height(), self.pixmap, 0, 0, self.pixmap.width(), self.pixmap.height())

        #The only one that "works."  I don't know why.
        #print(rect, end = ' ')
        #print(rect.toRect()) # This is the same scale as window geometry. Viewport coordinates? But not same x, y
        #print(self.sceneRect(), end = ' ')
        #print(self.sceneRect().toRect()) # This is *not* in normalized device coordinates
        #print(self.pos().x(), self.pos().y(), self.width(), self.height())
        #qp.drawPixmap(rect.toRect(), self.pixmap)

        #qp.drawPixmap(0, 0, self.scene.width(), self.scene.height(), self.pixmap, 0, 0, self.pixmap.width(), self.pixmap.height())
        #qp.drawPixmap(self.scene.sceneRect().toRect(), self.pixmap)
        #qp.drawPixmap(self.backgroundRect[0], self.pixmap)

       # #Run once.
       # if not self.bkgOriginX:
       #     self.bkgOriginX = int(rect.topLeft().x())
       #     self.bkgOriginY = int(rect.topLeft().y())

        # Update origin of coordinates
        if ((int(rect.width()) == qp.device().width()) and \
           (int(rect.height()) == qp.device().height())) or \
           not self.bkgOriginX:
            self.bkgOriginX = int(rect.topLeft().x())
            self.bkgOriginY = int(rect.topLeft().y())

        qp.drawPixmap(self.bkgOriginX, self.bkgOriginY, qp.device().width(), qp.device().height(), self.pixmap)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
