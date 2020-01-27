
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from results import Table
from excel import Excel
from visualize import Visualize
import os
import sys
from nlp import *
from nlp_nltk import *
import math
from textblob import TextBlob as tb

import itertools
from nltk.stem import porter


class SecondaryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        # Create widget
        label = QLabel(self)
        pixmap = QPixmap('vis1.svg')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
 
        self.show()

class MainWindow(QMainWindow):

    def tf(self,word, blob):
        return blob.words.count(word) / len(blob.words)

    def n_containing(self, word, bloblist):
        return sum(1 for blob in bloblist if word in blob.words)

    def idf(self, word, bloblist):
        return math.log(len(bloblist) / (1 + self.n_containing(word, bloblist)))

    def tfidf(self, word, blob, bloblist):
        return self.tf(word, blob) * self.idf(word, bloblist)
    
    xls = None
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        
        self.editor = QPlainTextEdit()  # Could also use a QTextEdit and set self.editor.setAcceptRichText(False)


        # Setup the QTextEdit editor configuration
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None
        
        layout.addWidget(self.editor)
    
        # Bottom layout setup #
        layout_bot = QGridLayout()
        
        self.comboBoxUS = QComboBox(self)
        self.comboBoxUS.currentIndexChanged.connect(self.US_index_changed)
        layout_bot.addWidget(self.comboBoxUS,0,0)
        
        self.addUSButton = QPushButton('add')
        self.addUSButton.setFixedWidth(80)
        self.addUSButton.clicked.connect(self.on_click_add_US_Name)
        layout_bot.addWidget(self.addUSButton,0,1)
  
        self.addDesButton = QPushButton('add')
        self.addDesButton.setFixedWidth(80)
        self.addDesButton.clicked.connect(self.on_click_add_DES)
        self.comboBoxDes = QComboBox(self)
        self.comboBoxDes.currentIndexChanged.connect(self.DES_index_changed)
        layout_bot.addWidget(self.comboBoxDes,1,0)
        layout_bot.addWidget(self.addDesButton,1,1)
        
        self.addACButton = QPushButton('add')
        self.addACButton.setFixedWidth(80)
        self.addACButton.clicked.connect(self.on_click_add_AC)
        self.comboBoxAC = QComboBox(self)
        layout_bot.addWidget(self.comboBoxAC,2,0)
        layout_bot.addWidget(self.addACButton,2,1)
        
        self.featureLabel = QLabel('Selected Feature: ')

        layout_bot.addWidget(self.featureLabel,3,0)
        
        layout.addLayout(layout_bot)  
        # end of bottom layout setup #
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(QIcon(os.path.join('images', 'blue-folder-open-document.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Edit")
        
        undo_action = QAction(QIcon(os.path.join('images', 'arrow-curve-180-left.png')), "Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon(os.path.join('images', 'arrow-curve.png')), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction(QIcon(os.path.join('images', 'scissors.png')), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon(os.path.join('images', 'document-copy.png')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join('images', 'clipboard-paste-document-text.png')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(QIcon(os.path.join('images', 'selection-input.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()
      
        edit_toolbar.addSeparator()
        
        stw_rem_action = QAction(QIcon(os.path.join('images', 'document-copy.png')), "Stop Words Removal", self)
        stw_rem_action.setStatusTip("Stop Words Removal")
        stw_rem_action.triggered.connect(self.on_click_rem_stop_words)
        edit_toolbar.addAction(stw_rem_action)
        
        stemmer_action = QAction(QIcon(os.path.join('images', 'document-copy.png')), "Porter Stemmer", self)
        stemmer_action.setStatusTip("Porter Stemmer")
        stemmer_action.triggered.connect(self.on_click_Stemmer)
        edit_toolbar.addAction(stemmer_action)
        
        visualize_action = QAction(QIcon(os.path.join('images', 'document-copy.png')), "visualize_action", self)
        visualize_action.setStatusTip("visualize_action")
        visualize_action.triggered.connect(self.on_click_visualize_action)
        edit_toolbar.addAction(visualize_action)
        
        cosine1_action = QAction(QIcon(os.path.join('images', 'nlp.png')), "cosine_similarity1", self)
        cosine1_action.setStatusTip("cosine_similarity1")
        cosine1_action.triggered.connect(self.on_click_cosine1_action)
        edit_toolbar.addAction(cosine1_action)
        
        cosine2_action = QAction(QIcon(os.path.join('images', 'nlp.png')), "cosine_similarity2", self)
        cosine2_action.setStatusTip("cosine_similarity1")
        cosine2_action.triggered.connect(self.on_click_cosine2_action)
        edit_toolbar.addAction(cosine2_action)
        
        jeccard_action = QAction(QIcon(os.path.join('images', 'nlp.png')), "jeccard_similarity", self)
        jeccard_action.setStatusTip("jeccard_similarity")
        jeccard_action.triggered.connect(self.on_click_jeccard_action)
        edit_toolbar.addAction(jeccard_action)
        
        tfidf_action = QAction(QIcon(os.path.join('images', 'nlp.png')), "tf-idf_similarity", self)
        tfidf_action.setStatusTip("tf-idf")
        tfidf_action.triggered.connect(self.on_click_tfidf_action)
        edit_toolbar.addAction(tfidf_action)
        
        TC_toolbar = QToolBar("TC")
        TC_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(TC_toolbar)
        edit_menu = self.menuBar().addMenu("&TC Options")
        
        """ check boxes """
        self.TC_Name_cb = QCheckBox('TC Name', self)
        self.TC_Name_cb.toggle()
        TC_toolbar.addWidget(self.TC_Name_cb)
        
        self.TC_Des_cb = QCheckBox('TC Description', self)
        self.TC_Des_cb.toggle()
        TC_toolbar.addWidget(self.TC_Des_cb)
        
        #remove stop words
        self.TC_RSW_cb = QCheckBox('Stop words remove on TC', self)
        self.TC_RSW_cb.toggle()
        TC_toolbar.addWidget(self.TC_RSW_cb)
        
        #porter stemmer
        self.TC_PS_cb = QCheckBox('Porter Stemmer on TC', self)
        self.TC_PS_cb.toggle()
        TC_toolbar.addWidget(self.TC_PS_cb)
        
        
        wrap_action = QAction(QIcon(os.path.join('images', 'arrow-continue.png')), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        self.update_title()
        self.show()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self):
        
        # open file open dialog
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Excel documents (*.xlsx);All files (*.*)")
        
        if (not path.endswith("xlsx")):
            QMessageBox.about(self, "Error", "Must choose excel file (.xlsx)")
            return
        # process excel file ( excel.py )
        self.xls = Excel(path)
        
        # Get all the sheet names that hold User stories and Test Cases
        self.comboBoxUS.addItems(self.xls.get_US_names())
       
        

    def file_save(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        text = self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);All files (*.*)")
        text = self.editor.toPlainText()

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
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("%s " % (os.path.basename(self.path) if self.path else "User Story to Test Case"))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode( 1 if self.editor.lineWrapMode() == 0 else 0 )
    
    def US_index_changed(self):
        """ Triggered by User Story combo-box change """
        self.comboBoxAC.clear()
        self.comboBoxDes.clear()
        self.comboBoxAC.clear()
        US = self.comboBoxUS.currentText()
        self.comboBoxDes.addItems(self.xls.get_US_Des(US))
        Dec = self.comboBoxDes.currentText()
        self.comboBoxAC.addItems(self.xls.get_Des_AC(Dec)) 
        self.featureLabel.setText("Current Feature: " + self.xls.get_FNUM(US))

    def DES_index_changed(self):
        """ Triggered by Description of User Story combo-box change """
        self.comboBoxAC.clear()
        Dec = self.comboBoxDes.currentText()
        self.comboBoxAC.addItems(self.xls.get_Des_AC(Dec)) 
     
    @pyqtSlot()
    def on_click_add_US_Name(self):
        """ Triggered by User Story add button """
        self.editor.appendPlainText(self.comboBoxUS.currentText())   
    
    def on_click_add_DES(self):
        """ Triggered by Description add button """
        self.editor.appendPlainText(self.comboBoxDes.currentText())  
        
    def on_click_add_AC(self):
        """ Triggered by Acceptance Criteria add button """
        self.editor.appendPlainText(self.comboBoxAC.currentText())    
        
    def on_click_tokenize(self):
        text = self.editor.toPlainText()
        text = tokenize(text)
    
    def on_click_rem_stop_words(self):
        """ Triggered by Remove Stop Words button - toolbar """
        text = self.editor.toPlainText()
        text = remove_stop_words(text)
        self.editor.setPlainText(text)
     
    def on_click_Stemmer(self):
        """ Triggered by Porter Stemmer button - toolbar """
        text = self.editor.toPlainText()
        text = Porter_Stemmer(text)
        self.editor.setPlainText(text)
     
    def on_click_visualize_action(self):
        """ Triggered by Visualize button - toolbar """
        #self.window = SecondaryWindow()
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "svg documents (*.svg);All files (*.*)")
        link = visualize(self.editor.toPlainText())

        if not path:
            # If dialog is cancelled, will return ''
            return
        
        try:
            with open(path, 'w') as f:
                f.write(link)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()
        
        self.dialog = Visualize(path)
        self.dialog.show()
     
    def on_click_cosine1_action(self):
        """ Triggered by Cosine Similarity1 button - toolbar """
        text = self.editor.toPlainText()
        if not text or text.isspace():
            QMessageBox.about(self, "Error", "Text box is empty. please choose a user story.")
            return
        if not self.xls:
            QMessageBox.about(self, "Error", "No  excel file  loaded.")
            return
        
        data = self.set_TC_data()     
        res = find_cosine(text,data)
        FNUM = self.featureLabel.text().split(' ')[-1]
        self.dialog = Table(res,FNUM)
        self.dialog.show()
           
    def on_click_cosine2_action(self):
        """ Triggered by Cosine Similarity2 button - toolbar """
        text = self.editor.toPlainText()
        if not text or text.isspace():
            QMessageBox.about(self, "Error", "Text box is empty. please choose a user story.")
            return
        if not self.xls:
            QMessageBox.about(self, "Error", "No  excel file  loaded.")
            return
        
        data = self.set_TC_data()
        res = find_cosine2(text, data)
        FNUM = self.featureLabel.text().split(' ')[-1]
        self.dialog = Table(res,FNUM)
        self.dialog.show()
 
    def on_click_jeccard_action(self):
        """ Triggered by Jeccard Similarity button - toolbar """
        text = self.editor.toPlainText()
        if not text or text.isspace():
            QMessageBox.about(self, "Error", "Text box is empty. please choose a user story.")
            return
        if not self.xls:
            QMessageBox.about(self, "Error", "No  excel file  loaded.")
            return
        
        data = self.set_TC_data()
        res = find_jeccard(text, data)
        FNUM = self.featureLabel.text().split(' ')[-1]
        self.dialog = Table(res,FNUM)
        self.dialog.show()   
    
    def on_click_tfidf_action(self):
        """ Triggered by tf-idf Similarity button - toolbar """
        text = self.editor.toPlainText()
        if not text or text.isspace():
            QMessageBox.about(self, "Error", "Text box is empty. please choose a user story.")
            return
        if not self.xls:
            QMessageBox.about(self, "Error", "No  excel file  loaded.")
            return
        
        numOfTopRes=5
        data = self.set_TC_data()
        tb_text=self.editor.toPlainText()
        res=find_tfidf_match(tb_text,data)
        FNUM = self.featureLabel.text().split(' ')[-1]
        self.dialog = Table(res,FNUM)
        self.dialog.show()   
        
    
    def set_TC_data(self):
        """ Sets data to compare from Test Cases. 
            - TC name only
            - TC Description only
            - TC name and description
        """
        data = []
        
        if (self.TC_Name_cb.isChecked() and self.TC_Des_cb.isChecked()):
            data = [[i[0], i[1]+" "+i[2]] for i in self.xls.get_TCs()]
        
        if (self.TC_Name_cb.isChecked() and not self.TC_Des_cb.isChecked()):
            data = [[i[0], i[1]] for i in self.xls.get_TCs()]
        
        if (not self.TC_Name_cb.isChecked() and self.TC_Des_cb.isChecked()):
            data = [[i[0], i[2]] for i in self.xls.get_TCs()]
        
        # if remove stop word toggle is on
        if (self.TC_RSW_cb.isChecked()):
            for tc in data:
                tc[1] = remove_stop_words(tc[1])
                #tc = [tc[0], remove_stop_words(tc[1])]
                
        # if porter stemmer toggle is on
        if (self.TC_PS_cb.isChecked()):
            for tc in data:
                #tc = [tc[0], Porter_Stemmer(tc[1])]
                tc[1] = Porter_Stemmer(tc[1])
                     
        return data

    
    
      
if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName("No2Pads")

    window = MainWindow()
    app.exec_()
