#!/usr/bin/python3.5
#Always run this with python3.5

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QActionGroup,
                             QFontComboBox, QComboBox, QWidget, QVBoxLayout)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtQuick import QQuickView
from PyQt5.QtGui import QFontDatabase, QIcon, QFont

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.view = TextView()
        self.centralWidget = QWidget(self)
        self.layout = QVBoxLayout(self.centralWidget)

        self.view.statusChanged.connect(self.quickViewStatusChanged)
        self.view.sceneGraphError.connect(self.sceneGraphError)

        self.container = QWidget.createWindowContainer(self.view)
        self.container.setMinimumSize(self.view.size())
        self.container.setFocusPolicy(Qt.TabFocus)
        self.layout.addWidget(self.container)

        self.setCentralWidget(self.centralWidget)
        self.statusBar().showMessage('Ready')

        self.toolbar = self.addToolBar('Text Effects')

        # Set up the text effects tools
        actionGroup = QActionGroup(self)

        noneAction = QAction(QIcon("none.png"), "&Clear", self)
        noneAction.setStatusTip("Clear Effects")
        #noneAction.triggered.connect(self.view.noEffect)
        actionGroup.addAction(noneAction)

        blurAction = QAction(QIcon("blur.png"), "&Blur", self)
        blurAction.setStatusTip("Blur Text")
        #blurAction.triggered.connect(self.view.blur)
        actionGroup.addAction(blurAction)

        opacityAction = QAction(QIcon("opacity.png"), "&Transparency", self)
        opacityAction.setStatusTip("Fade Text")
        #opacityAction.triggered.connect(self.view.opacity)
        actionGroup.addAction(opacityAction)

        shadowAction = QAction(QIcon("shadow.png"), "&Drop Shadow", self)
        shadowAction.setStatusTip("Drop-shadow Text")
        #shadowAction.triggered.connect(self.view.shadow)
        actionGroup.addAction(shadowAction)

        self.toolbar.addActions(actionGroup.actions())
        self.toolbar.addSeparator()

        # Set up the font selection tools
        boldAction = QAction(QIcon("bold.png"), "&Bold", self)
        boldAction.setStatusTip("Bold Text")
        boldAction.setCheckable(True)
        boldAction.setChecked(True)
        #boldAction.triggered[bool].connect(self.view.bold)
        self.toolbar.addAction(boldAction)

        italicAction = QAction(QIcon("italic.png"), "&Italic", self)
        italicAction.setStatusTip("Italic Text")
        italicAction.setCheckable(True)
        #italicAction.triggered[bool].connect(self.view.italic)
        self.toolbar.addAction(italicAction)

        self.fontBox = QFontComboBox(self)
        self.fontBox.setCurrentFont(QFont("PT Sans", 16, QFont.Bold))
        #self.fontBox.currentFontChanged.connect(self.view.fontFamily)
        self.toolbar.addWidget(self.fontBox)

        self.fontSizeBox = QComboBox(self)
        self.fontSizeBox.setEditable(True)
        strlist = []
        intlist = QFontDatabase.standardSizes()
        for item in intlist:
            strlist.append(str(item))
        self.fontSizeBox.addItems(strlist)
        self.fontSizeBox.setCurrentText("16")
        #self.fontSizeBox.currentTextChanged.connect(self.view.fontSize)
        self.toolbar.addWidget(self.fontSizeBox)

        self.setGeometry(300, 300, 600, 500)
        self.setWindowTitle('Renderer')
        self.show()


    def quickViewStatusChanged(status):
        if status is QQuickView.Error:
            errors = []
            for error in self.quickView.errors():
                errors.append(str(error))
            self.statusBar().showmessage((', ').join(errors))


    def sceneGraphError(error, message):
        self.statusBar.showMessage(message)


class TextView(QQuickView):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.setResizeMode(QQuickView.SizeRootObjectToView)
        self.setSource(QUrl("screen.qml"))


    def readSong(self, filename):

        try:
            with open(filename, 'r') as f:
                song = {}
                verseOrder = []
                slide = []
                label = ''
                for line in f:
                    if '-author:' in line:
                        self.author = line.partition(':')[2]
                        self.author = self.author.rstrip('\n')
                    elif '-copyright:' in line:
                        self.copyright = line.partition(':')[2]
                        self.copyright = self.copyright.rstrip('\n')
                    elif '---[' in line:
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
