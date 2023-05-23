from PyQt5.QtWidgets import (QLabel, QTextEdit, QLineEdit, QToolButton, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator

class Button(QToolButton):

    def __init__(self, text, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setText(text)
        self.clicked.connect(callback)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 5)
        size.setWidth(size.width()+20)
        return size

class DateLineEdit(QLineEdit):

    def __init__(self):
        super().__init__()
        self.setValidator(QIntValidator())
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.setAlignment(Qt.AlignCenter)
    
    def sizeHint(self):
        size = super(DateLineEdit, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(size.width()-80)
        return size

class CalcLineEdit(QLineEdit):

    def __init__(self):
        super().__init__()
        # self.setValidator(QDoubleValidator(bottom=0, decimals=3))
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        font = self.font()
        font.setPointSize(font.pointSize() + 4)
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignCenter)
    
    def sizeHint(self):
        size = super(CalcLineEdit, self).sizeHint()
        size.setHeight(size.height()+10)
        size.setWidth(size.width()+37)
        return size
    
class BigBoldText(QLabel):

    def __init__(self, text):
        super().__init__()
        tempFont = self.font()
        self.setText(text)
        tempFont.setPointSize(13)
        tempFont.setBold(True)
        self.setFont(tempFont)
        self.setAlignment(Qt.AlignCenter)

class ChartTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAcceptRichText(True)
        self.setReadOnly(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setAlignment(Qt.AlignCenter)
    
    def sizeHint(self):
        size = super(ChartTextEdit, self).sizeHint()
        size.setHeight(size.height()+300)
        size.setWidth(size.width()+280)
        return size