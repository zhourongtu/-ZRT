# -*- coding: utf-8 -*-
import sys
import mysql.connector
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

class StudentQueryFrame(QWidget):
    def __init__(self, id):
        super(StudentQueryFrame, self).__init__()
        self.id = id
        self.__back_btn = None
        self.__query_btn = None
        
        # 数据库连接
        self.conn = mysql.connector.connect(user = 'root', password = '123456', database = 'studentgrademanagement', use_unicode=True)
        self.cursor = self.conn.cursor()

        # 初始化
        self.init_ui_Query_Frame()
        
        # 默认搜索
        self.query()

    def init_ui_Query_Frame(self):
        self.resize(700, 400)
        self.setWindowTitle("学生查询界面")

        self.layout = QVBoxLayout()

        self.HLayout1 = QHBoxLayout()
        self.HLayout2 = QHBoxLayout()
        self.HLayout3 = QHBoxLayout()

    # 布局1 返回+空白label
        self.__back_btn = QPushButton("返回", self)
        self.__back_btn.setFixedSize(50, 30)
        # self.__back_btn.clicked.connect(...)
        self.HLayout1.addWidget(self.__back_btn)
        self.HLayout1.addStretch(1)
    
    # 布局2 学年+列表+课程号+列表+学期+text图+查询按钮
        # 标签：学年 + 下拉列表
        self.__academic_year_label = QLabel(self)
        self.__academic_year_label.setText("学年:")
        self.__academic_year_comboBox = QComboBox(self)
        self.__academic_year_comboBox.addItem("")
        self.__academic_year_comboBox.addItem("2017")
        self.__academic_year_comboBox.addItem("2018")
        self.__academic_year_comboBox.addItem("2019")
        self.__academic_year_comboBox.addItem("2020")
        
        # 标签：学期 + 下拉列表
        self.__semester_label = QLabel(self)
        self.__semester_label.setText("学期：")
        self.__semester_comboBox = QComboBox(self)
        self.__semester_comboBox.addItem("")
        self.__semester_comboBox.addItem("春夏")
        self.__semester_comboBox.addItem("秋冬")
        
        # 标签：课程号 + 输入框
        self.__course_id_label = QLabel(self)
        self.__course_id_label.setText("课程号：")
        self.__course_id_LineEdit = QLineEdit(self)
        self.__course_id_LineEdit.setPlaceholderText("请输入课程号")
        
        # 查询按钮
        self.__query_btn = QPushButton("查询", self)
        self.__query_btn.clicked.connect(self.query)

        self.HLayout2.addWidget(self.__academic_year_label)
        self.HLayout2.addWidget(self.__academic_year_comboBox)
        self.HLayout2.addWidget(self.__semester_label)
        self.HLayout2.addWidget(self.__semester_comboBox)
        self.HLayout2.addWidget(self.__course_id_label)
        self.HLayout2.addWidget(self.__course_id_LineEdit)
        self.HLayout2.addWidget(self.__query_btn)
        self.HLayout2.addStretch(1)

    # 布局3 表格
        self.__form_course_view = QTableView()
        self.__form_course_view.horizontalHeader().setStretchLastSection(True)
        self.__form_course_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.__form_course_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__form_course_model = QStandardItemModel(100, 3)
        self.__set_form_header()
        self.__form_course_view.setModel(self.__form_course_model)

        self.HLayout3.addWidget(self.__form_course_view)

    # 拼接
        self.layout.addLayout(self.HLayout1)
        self.layout.addLayout(self.HLayout2)
        self.layout.addLayout(self.HLayout3)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    # 设置表格头
    def __set_form_header(self):
        self.__form_course_model.setHorizontalHeaderLabels(["课程号", "课程名", "成绩"])
        

    # 查询。 按学年查询，按学年+学期查询，按课程查询
    def query(self):
        academic_year = self.__academic_year_comboBox.currentText()
        semester = self.__semester_comboBox.currentText()
        course_id = self.__course_id_LineEdit.text()        
        print(academic_year, semester, course_id)
        sql = '''select coursechoosing.course_id, course.course_name, coursechoosing.grade from coursechoosing, course where coursechoosing.course_id = course.course_id and coursechoosing.id = '{}'
            '''.format(self.id)
        if(len(course_id) != 0):
            # 按照课程id搜索
            if(len(academic_year) != 0 or len(semester) != 0):
                messagebox = QMessageBox.about(self, u'提示', u'\n查询课程号时，请不要选择学年与学期！')
            else:
                sql = sql + 'and course.course_id = {}'.format(course_id)
        elif(len(academic_year) == 0 and len(semester) != 0):
            # 默认搜索
            pass
        else:
            # 按学年与学期搜索（可单独学年，可单独学期）
            if(len(academic_year) != 0):
                sql = sql + 'and course.academicYear = \'{}\''.format(academic_year)
            if(len(semester) != 0):
                sql = sql + 'and course.semester = \'{}\' '.format(semester)

        print(sql)
        try:
            self.cursor.execute(sql)
        except Exception:
            pass
        finally:
            pass
        info = self.cursor.fetchall()
        self.__form_course_model.clear()
        self.__set_form_header()
        for row in range(len(info)):
            for column in range(3):
                item = QStandardItem("%s"%(str(info[row][column])))
                self.__form_course_model.setItem(row, column, item)
        # 设置表格
        print(info)
        




def main():
    app = QApplication(sys.argv)
    w = StudentQueryFrame(1)
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
