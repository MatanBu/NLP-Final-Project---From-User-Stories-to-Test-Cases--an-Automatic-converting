import sys
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random
 
class Vis(QMainWindow):
    data = []
    def __init__(self, data):
        super().__init__()
        Vis.data = data
        self.left = 10
        self.top = 10
        self.title = 'Results Graph'
        self.width = 640
        self.height = 400
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        m = PlotCanvas(self, width=5, height=4)
        m.move(0,0)
 
        
 
        self.show()
         
class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(Vis.data)
 
 
    def plot(self,data):
        ydata = [data[i][1] for i in range(len(data))]
        ax = self.figure.add_subplot(111)
        ax.plot(ydata, 'r-')
        ax.set_title('results')
        self.draw()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Vis()
    sys.exit(app.exec_())