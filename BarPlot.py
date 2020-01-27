import sys
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

class VisBar(QMainWindow):
    data = []
    def __init__(self, data):
        super().__init__()
        VisBar.data = data
        self.left = 10
        self.top = 10
        self.title = 'Results Graph'
        self.width = 640
        self.height = 400
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        BarPlot(VisBar.data)
        

class BarPlot():
    
    def __init__(self,data):
        objects = [i for i in range(len(data))]
        performance  = [data[i][1] for i in range(len(data))]
        y_pos = np.arange(len(objects))
        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('Score')
        plt.xlabel("TC#")
        plt.title('Results')
 
        plt.show()