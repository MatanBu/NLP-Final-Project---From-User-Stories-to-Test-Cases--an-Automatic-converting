import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QPushButton, QFileDialog, QGridLayout,\
    QPlainTextEdit, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from cytoolz.tests.test_functoolz import double
from PyQt5.Qt import QLabel
from vis import Vis
from BarPlot import VisBar
from statistics import stats
 
class Table(QWidget):
 
    def __init__(self,data,fnum):
        super().__init__()
        self.data = data
        self.us_fnum = fnum
        self.title = 'results table'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        layout_top = QGridLayout()
        
        self.button = QPushButton('Save As', self) 
        self.button.clicked.connect(self.file_saveas)
        
        self.button_stats = QPushButton('Show Stats', self) 
        self.button_stats.clicked.connect(self.stats)
        
        self.button_plot = QPushButton('Plot', self) 
        self.button_plot.clicked.connect(self.plot)
        
        self.button_barplot = QPushButton('Bar Plot', self) 
        self.button_barplot.clicked.connect(self.barPlot)
        
        self.minValLabel = QLabel('Minimal Similarity:')
        self.minValText = QLineEdit(self)
        self.minValText.resize(40,25)
        
        layout_top.addWidget(self.button,0,0)
        layout_top.addWidget(self.button_stats,1,0)
        layout_top.addWidget(self.button_plot,2,0)
        layout_top.addWidget(self.button_barplot,3,0)
        layout_top.addWidget(self.minValLabel,4,0)
        layout_top.addWidget(self.minValText,4,1)
        
        
        self.createTable()
 
        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        #self.layout.addWidget(self.button)
        #self.layout.addWidget(self.button_stats)
        self.layout.addLayout(layout_top)
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 
 
        # Show widget
        self.show()
 
    def createTable(self):
        """ 
            Creates table from received data
            
            [0] TC, [1] Similarity Score
            
        """
        length = len(self.data)
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(length)
        self.tableWidget.setColumnCount(2)
        for i in range(length):
            self.tableWidget.setItem(i,0, QTableWidgetItem(str(self.data[i][0])))
            self.tableWidget.setItem(i,1, QTableWidgetItem(str(self.data[i][1])))
             
        self.tableWidget.move(0,0)
 
        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)
 
    def stats(self):
        
        self.dialog = stats(self.data,self.us_fnum)
        self.dialog.show()   
        """
        sim_high = 0.7 # dsadasd
        sim_correct_count = 0
        sim_wrong_count = 0
        sim_total = self.tableWidget.rowCount()
        
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
        
        print("Accuracy from above 70%:  " + str(float(sim_correct_count/sim_high)))
        print("Accuracy from total (over 70% and correct) :" + str(float((sim_correct_count+sim_wrong_count)/sim_total)))
        """
        
        
    @pyqtSlot()
    def on_click(self):
        print("\n")
        
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
        
    @pyqtSlot()
    def plot(self):
        
        self.dialog = Vis(self.data)
        self.dialog.show()
        
    @pyqtSlot()
    def barPlot(self):
        
        self.dialog = VisBar(self.data)
        self.dialog.show()   
         
            
    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);All files (*.*)")
        text = ""
        for tup in self.data:
            text += str(tup) + "\n"

        if not path:
            # If dialog is cancelled, will return ''
            return

        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
              
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Table()
    sys.exit(app.exec_())           
            
            