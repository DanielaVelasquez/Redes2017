import sys
from PyQt4.QtGui import *

class ButtonImage(QPushButton):
    def __init__(self,picture):
        super(ButtonImage, self).__init__()
        self.picture = picture

    def paintEvent(self, event):
                painter = QPainter(self)
                painter.drawPixmap(event.rect(), self.picture)

    def sizeHint(self):
                return self.picture.size()

