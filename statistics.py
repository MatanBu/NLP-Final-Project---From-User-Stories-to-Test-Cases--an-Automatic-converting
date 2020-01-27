import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QPushButton, QFileDialog, QGridLayout,\
    QPlainTextEdit, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class stats(QWidget):
 
    def __init__(self,data,fnum):
        super().__init__()
        self.data = data
        self.us_fnum = fnum
        self.title = 'statistics'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.editor = QPlainTextEdit()
        self.editor.move(20,20)
        self.editor.resize(280,200)
        
        self.editor.show()
        # Show widget
    def calcStats(self):
        
        ans = ""
        sim_high = 0.7 
        sim_correct_count = 0
        sim_wrong_count = 0
        sim_total = len(self.data)
        
        min_sim = str(self.minValText.text())
        if min_sim != '':
            min_sim = float(min_sim)
        else:
            min_sim = 0.7 #default
        
        for row in range(self.tableWidget.rowCount()):
            
            tc = str(self.tableWidget.item(row, 0).text())
            scr = float(str(self.tableWidget.item(row, 1).text()))
            if scr > min_sim:
                sim_high+=1
                if (tc.partition(' ')[0] == self.us_fnum):
                    #print('similar: ' + tc)
                    sim_correct_count+=1
                else:
                    #print('not similar: ' + tc)
                    sim_wrong_count+=1    
        
        ans += ("Accuracy from above 70%:  " + str(float(sim_correct_count/sim_high)) + "\n")
        ans += ("Accuracy from total (over 70% and correct) :" + str(float((sim_correct_count+sim_wrong_count)/sim_total)) + "\n")    
        
        return ans
        