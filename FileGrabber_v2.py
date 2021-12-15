from PyQt5.QtWidgets import QApplication,QLineEdit,QWidget,QFormLayout,QLabel,QPushButton,QMessageBox
from PyQt5.QtGui import QFont,QIntValidator
import os.path, pathlib, sys, shutil, multiprocessing as mp


class GUI(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        # Window title
        self.setWindowTitle("File Grabber")
        self.setStyleSheet("background-color: #082032; color:#f4f4f4;")
        self.resize(270, 175)

        #Window label and input field
        self.label = QLabel('*** Welcome to File Grabbing Tool ***')
        self.label.setStyleSheet("color:#f4f4f4; ")
        self.e1 = QLineEdit()
        self.e1.setFont(QFont("Calibri",10))
        self.e1.setStyleSheet("color:#f4f4f4;")
        
        self.e2 = QLineEdit()
        self.e2.setFont(QFont("Calibri",10))
        self.e2.setStyleSheet("color:#f4f4f4;")
        
        self.e3 = QLineEdit()
        self.e3.setFont(QFont("Calibri",10))
        self.e3.setStyleSheet("color:#f4f4f4;")
        self.e3.setValidator(QIntValidator())
        
        self.e4 = QLineEdit()
        self.e4.setFont(QFont("Calibri",10))
        self.e4.setStyleSheet("color:#f4f4f4;")
        self.e4.setValidator(QIntValidator())

        # Button for capturing 
        self.button = QPushButton('Submit', self)
        self.button.setFont(QFont("Calibri",10))
        self.button.setStyleSheet("color:white; \
                                    background-color:#FFC400;")
        self.button.move(265,140)
        self.button.clicked.connect(self.on_click)
        self.show()

        #form Layout
        self.flo = QFormLayout()
        self.flo.addRow("" , self.label)

        self.label2 = QLabel("Enter the File Format")
        self.label2.setStyleSheet("color:#f4f4f4;")
        self.flo.addRow(self.label2,self.e1)
        
        self.label3 = QLabel("Enter Exact file Name")
        self.label3.setStyleSheet("color:#f4f4f4;")
        self.flo.addRow(self.label3,self.e2)

        self.label4 = QLabel("Enter Range Starting point ")
        self.label4.setStyleSheet("color:#f4f4f4;")
        self.flo.addRow(self.label4,self.e3)

        self.label5 = QLabel("Enter Range ending point")
        self.label5.setStyleSheet("color:#f4f4f4;")
        self.flo.addRow(self.label5,self.e4)

        self.setLayout(self.flo)
    
    def flatten_list(self,nested_list):
        if any(isinstance(i, list) for i in nested_list):
            flatten_li = sum(nested_list, [])
            return flatten_li
        else:
            return nested_list

    def range_cal(self,flatten_li,final_range):
        try:
            while len(flatten_li) > final_range:
                flatten_li.pop()
           
            return flatten_li    
        except:
            QMessageBox.warning(self, 'Try Again', "\t  Enter Write format:"  )

    def find(self,valid_format, e_file_name = None, range_in = None, range_en = None):
        nested_list = []
        flag = False

        import win32api as win
        drive_li = win.GetLogicalDriveStrings().split('\000')
        for ind,drive in enumerate(drive_li):
            try:
                if e_file_name =='' and range_in =='' and range_en =='' :
                    self.li = sorted(pathlib.Path(drive).glob('**/**/*.'+valid_format+''))
                    nested_list.append(self.li)
                   
                elif e_file_name and range_in =='' and range_en =='':
                    self.li = sorted(pathlib.Path(drive).glob('**/**/*' + e_file_name +'.'+valid_format+''))
                    nested_list.append(self.li)
                   
                elif range_in and range_en and e_file_name == '' :
                    final_range = int(range_in) + int(range_in)
                    self.li = sorted(pathlib.Path(drive).glob('**/**/*' +'.'+valid_format+''))
                    nested_list.append(self.li)
                    flag = True

                else:
                    QMessageBox.warning(self, 'Try Again', "\t  Enter Write format:"  )
            except:
                pass
            
        if ind == len(drive_li) - 1:
            flatten_li = self.flatten_list(nested_list)
            if flag:
                poped_li = self.range_cal(flatten_li,final_range)
                self.copy_file(poped_li)
            else:
                self.copy_file(flatten_li)
        
        
    #File Copying
    def copy_file(self,flatten_list):
        dst = os.getcwd()
        for sub_li in flatten_list:
            if os.path.isdir(dst):
                dst = os.path.join(dst, os.path.basename(sub_li))
                print(f'This is destination {dst}, and this sub_li {sub_li}')
                shutil.copyfile(sub_li, dst)
                dst = os.getcwd() 
        
    def on_click(self):
        self.file_format = self.e1.text()
        e_file_name = self.e2.text()
        range_in = self.e3.text()
        range_en = self.e4.text()
        
        files_format = ['pdf','doc','txt','xlx','xlsx','exe','docx','bin','BAK','bat','tmp'\
                        ,'GHO','log','gif','png','jpg','jpeg','py','bat','csv','java','BMP','ppt'\
                        ,'pptx','zip','wav','tar','avi','iso','html']

        valid_format = " ".join([self.file_format for i in files_format if i == self.file_format])  

        if valid_format != '':
     
            QMessageBox.information(self, 'Confirm Yours Information', "You typed: " + self.file_format, QMessageBox.Ok, QMessageBox.Ok)
            self.find(valid_format, e_file_name, range_in, range_en)
            self.e1.setText(""),self.e2.setText(""),self.e3.setText(""),self.e4.setText("")
   
        else:
            QMessageBox.warning(self, 'Try Again', "\t  Enter file format:"  )
            QMessageBox.warning(self, 'Try Again', "\t  You Typed wrong Format:" + self.file_format  + """
                You Should have enter the following format:
                - pdf       -png
                - doc       -jpg
                - txt       -jpeg
                - xlx       -py       
                - xlsx      -bat
                - exe       -csv
                - docx      -java
                - bin       -BMP
                - BAK       -ppt
                - bat       -pptx
                - tmp       -zip
                - GHO       -wav
                - log       -tar
                - gif       -html
            """)
            # QMessageBox

            self.e1.setText(""),self.e2.setText("")

if __name__ == "__main__":
        app = QApplication(sys.argv)
        win = GUI()
        win.show()
        sys.exit(app.exec_())
        