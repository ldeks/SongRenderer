#!/usr/bin/python3.5
#Always run this with python3.5

import sys
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGraphicsBlurEffect, QGraphicsOpacityEffect, QGraphicsDropShadowEffect,
                             QMainWindow, QAction, QActionGroup, QFontComboBox, QComboBox)
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPixmap, QFont, QColor, QMatrix4x4, QIcon, QFontDatabase

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.view = TextView(self)
        self.setCentralWidget(self.view)

        self.toolbar = self.addToolBar('Text Effects')

        # Set up the text effects tools
        actionGroup = QActionGroup(self)

        noneAction = QAction(QIcon("none.png"), "&Clear", self)
        noneAction.setStatusTip("Clear Effects")
        noneAction.triggered.connect(self.view.noEffect)
        actionGroup.addAction(noneAction)

        blurAction = QAction(QIcon("blur.png"), "&Blur", self)
        blurAction.setStatusTip("Blur Text")
        blurAction.triggered.connect(self.view.blur)
        actionGroup.addAction(blurAction)

        opacityAction = QAction(QIcon("opacity.png"), "&Transparency", self)
        opacityAction.setStatusTip("Fade Text")
        opacityAction.triggered.connect(self.view.opacity)
        actionGroup.addAction(opacityAction)

        shadowAction = QAction(QIcon("shadow.png"), "&Drop Shadow", self)
        shadowAction.setStatusTip("Drop-shadow Text")
        shadowAction.triggered.connect(self.view.shadow)
        actionGroup.addAction(shadowAction)

        self.toolbar.addActions(actionGroup.actions())
        self.toolbar.addSeparator()

        # Set up the font selection tools
        boldAction = QAction(QIcon("bold.png"), "&Bold", self)
        boldAction.setStatusTip("Bold Text")
        boldAction.setCheckable(True)
        boldAction.setChecked(True)
        boldAction.triggered[bool].connect(self.view.bold)
        self.toolbar.addAction(boldAction)

        italicAction = QAction(QIcon("italic.png"), "&Italic", self)
        italicAction.setStatusTip("Italic Text")
        italicAction.setCheckable(True)
        italicAction.triggered[bool].connect(self.view.italic)
        self.toolbar.addAction(italicAction)

        self.fontBox = QFontComboBox(self)
        self.fontBox.setCurrentFont(QFont("PT Sans", 16, QFont.Bold))
        self.fontBox.currentFontChanged.connect(self.view.fontFamily)
        self.toolbar.addWidget(self.fontBox)

        self.fontSizeBox = QComboBox(self)
        self.fontSizeBox.setEditable(True)
        strlist = []
        intlist = QFontDatabase.standardSizes()
        for item in intlist:
            strlist.append(str(item))
        self.fontSizeBox.addItems(strlist)
        self.fontSizeBox.setCurrentText("16")
        self.toolbar.addWidget(self.fontSizeBox)


        self.setGeometry(300, 300, 600, 500)
        self.setWindowTitle('Renderer')
        self.show()


class TextView(QGraphicsView):

    def __init__(self, parent):
        super().__init__(parent)

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

        self.currentSlide = 0
        if self.readSong('praise-to-the-lord'):
            self.unrollSong()
            self.text = self.scene.addText(self.slides[0], self.font)
        else:
            self.text = self.scene.addText("Praise to the Lord\nThe Almighty\nThe King of Creation", self.font)
        self.text.setDefaultTextColor(QColor(255, 255, 255))
        self.text.setFlags(QGraphicsItem.ItemIsSelectable |
                           QGraphicsItem.ItemIsMovable)

        self.setScene(self.scene)

    def resizeEvent(self, e):

        self.adjustText()
        self.scene.setSceneRect(QRectF(self.viewport().rect()))
        self.centerText()

    def keyPressEvent(self, e):


        if e.key() == Qt.Key_Right:
            self.currentSlide += 1
            if self.currentSlide >= len(self.slides):
                #Loop to beginning
                self.currentSlide = 0
            self.text.setPlainText(self.slides[self.currentSlide])
            self.adjustText()
            self.centerText()

        elif e.key() == Qt.Key_Left:
            self.currentSlide -= 1
            if self.currentSlide < 0:
                #Loop to end
                self.currentSlide = len(self.slides) - 1
            self.text.setPlainText(self.slides[self.currentSlide])
            self.adjustText()
            self.centerText()


    def blur(self):

        shadow = QGraphicsBlurEffect()
        shadow.setBlurRadius(self.shadowSize)
        self.text.setGraphicsEffect(shadow)


    def shadow(self):

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(self.shadowSize)
        shadow.setOffset(self.shadowOffset)
        self.text.setGraphicsEffect(shadow)


    def opacity(self):

        self.text.setGraphicsEffect(QGraphicsOpacityEffect())


    def noEffect(self):

        self.text.setGraphicsEffect(None)


    def bold(self, enabled):

        self.font.setBold(enabled)
        self.adjustText()
        self.centerText()


    def italic(self, enabled):

        self.font.setItalic(enabled)
        self.adjustText()
        self.centerText()

    def fontFamily(self, font):

        self.font.setFamily(font.family())
        self.adjustText()
        self.centerText()


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

    def readSong(self, filename):

        try:
            with open(filename, 'r') as f:
                song = {}
                verseOrder = []
                slide = []
                label = ''
                for line in f:
                    if '---[' in line:
                        start = len('---[')
                        end = line.find(']---')
                        label = line[start:end]
                        label = label.replace(':', ' ')
                        if label not in song:
                            song[label] = []
                            verseOrder.append(label)
                        if slide:
                            #Flush slide
                            slideStr = ('').join(slide)
                            #Get rid of that last newline
                            slideStr = slideStr.rstrip('\n')
                            song[label].append(slideStr)
                            slide = []
                    else:
                        slide.append(line)

                #Flush last slide
                slideStr = ('').join(slide)
                #Get rid of that last newline
                slideStr = slideStr.rstrip('\n')
                song[label].append(slideStr)

                self.song = song
                self.verseOrder = verseOrder
                return True
        except(FileNotFoundError):
            print('%s not found' % filename)
            return False


    def unrollSong(self):

        self.slides = []
        for label in self.verseOrder:
            for item in self.song[label]:
                self.slides.append(item)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    mwindow = MainWindow()
    sys.exit(app.exec_())
