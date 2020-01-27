import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase, QPainter, QFont
from PyQt5 import QtSvg

class Visualize(QWidget):
 
    def __init__(self,path):
        super().__init__()
        self.path = path
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.widget = QtSvg.QSvgWidget()
        self.widget.load(self.path)
        
        self.large_font = QFont("Arial", 12)
        #self.fixedFont = QFontDatabase.pointSizes("Arial", 12)
        self.widget.setFont(self.large_font)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout) 
        
        self.show()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Visualize("visu/1.svg")
    sys.exit(app.exec_())