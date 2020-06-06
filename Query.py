from  Ui_query import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtGui import *

class Query_Frame(QMainwindow, Ui_MainWindow):
    def __init__(self):
        
        super(Query_Frame, self).__init__()
        self.setupUi(self)
        

    