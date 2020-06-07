# -*- coding: utf-8 -*-
import sys
import mysql.connector
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from modify_grade_dialog import modify_grade_dialog

class TeacherQueryFrame(QWidget):
    def __init__(self, id):
        super(TeacherQueryFrame, self).__init__()
        self.id = id
        self.__back_btn = None
        self.__query_course_btn = None
        self.__modify_btn = None
        
        # 数据库连接
        self.conn = mysql.connector.connect(user = 'root', password = '123456', database = 'studentgrademanagement', use_unicode=True)
        self.cursor = self.conn.cursor()

        # 初始化
        self.init_ui_Query_Frame()
        
        # 默认搜索
        self.query_course()

    def init_ui_Query_Frame(self):
        self.resize(700, 400)
        self.setWindowTitle("学生查询界面")

        self.layout = QVBoxLayout()

        self.HLayout1 = QHBoxLayout()
        self.HLayout2 = QHBoxLayout()
        self.HLayout3 = QHBoxLayout()
        self.HLayout4 = QHBoxLayout()

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
        
        # 查询课程按钮
        self.__query_course_btn = QPushButton("课程查询", self)
        self.__query_course_btn.clicked.connect(self.query_course)
        # 查询学生按钮
        self.__query_student_btn = QPushButton("学生成绩查询")
        self.__query_student_btn.clicked.connect(self.query_student)

        # 布局添加
        self.HLayout2.addWidget(self.__academic_year_label)
        self.HLayout2.addWidget(self.__academic_year_comboBox)
        self.HLayout2.addWidget(self.__semester_label)
        self.HLayout2.addWidget(self.__semester_comboBox)
        self.HLayout2.addWidget(self.__course_id_label)
        self.HLayout2.addWidget(self.__course_id_LineEdit)
        self.HLayout2.addWidget(self.__query_course_btn)
        self.HLayout2.addWidget(self.__query_student_btn)
        self.HLayout2.addStretch(1)

    # 布局3 成绩段查询：框框-框框 + 修改成绩框
        self.__grade_label = QLabel(self)
        self.__grade_label.setText("成绩段查询")
        self.__grade_edit_low = QLineEdit(self)
        self.__grade_edit_low.setPlaceholderText("最低区间")
        self.__useless1_label = QLabel(self)
        self.__useless1_label.setText("-")
        self.__grade_edit_high = QLineEdit(self)
        self.__grade_edit_high.setPlaceholderText("最高区间")
        self.__modify_btn = QPushButton("修改学生成绩")
        self.__modify_btn.clicked.connect(self.modify_grade)
        self.HLayout3.addStretch(1)
        self.HLayout3.addWidget(self.__grade_label)
        self.HLayout3.addWidget(self.__grade_edit_low)
        self.HLayout3.addWidget(self.__useless1_label)
        self.HLayout3.addWidget(self.__grade_edit_high)
        self.HLayout3.addWidget(self.__modify_btn)


    # 布局4 表格
        self.__form_view = QTableView()
        self.__form_view.horizontalHeader().setStretchLastSection(True)
        self.__form_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.__form_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.HLayout4.addWidget(self.__form_view)
    # 拼接
        self.layout.addLayout(self.HLayout1)
        self.layout.addLayout(self.HLayout2)
        self.layout.addLayout(self.HLayout3)
        self.layout.addLayout(self.HLayout4)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    # 布局4的表格-->course表格

    # 查询自己所教过的课程（只显示课程，课程id，课程名，学期，学年， 教师名
    def __set_form_course(self, data):
        self.__form_course_model = QStandardItemModel(100, 5) # 模型
        self.__form_course_model.setHorizontalHeaderLabels(["课程id", "课程名", "学期", "学年", "老师名"]) # 名称
        for row in range(len(data)):
            for column in range(5):
                item = QStandardItem("%s"%(str(data[row][column])))
                self.__form_course_model.setItem(row, column, item)

        self.__form_view.setModel(self.__form_course_model)

    # 查询该课程的学生成绩。课程
    def __set_form_student(self, data):
        self.__form_course_model = QStandardItemModel(100, 5) # 模型
        self.__form_course_model.setHorizontalHeaderLabels(["学生学号", "学生名字", "课程ID", "课程名", "成绩"]) # 名称
        for row in range(len(data)):
            for column in range(5):
                item = QStandardItem("%s"%(str(data[row][column])))
                self.__form_course_model.setItem(row, column, item)

        self.__form_view.setModel(self.__form_course_model)
        
    # 得到查询信息（需要复用）
    def __get_query_info(self):
        self.__academic_year = self.__academic_year_comboBox.currentText() # 学年
        self.__semester = self.__semester_comboBox.currentText() # 学期
        self.__course_id = self.__course_id_LineEdit.text() # 课程号
        self.__grade_low = self.__grade_edit_low.text() # 最低分数
        self.__grade_high = self.__grade_edit_high.text() # 最高分数

    # 查询课程，按课程号，学期，学年查询
    def query_course(self):
        self.__get_query_info()
        # 查询自己教授的所有课程
        sql = '''select course.course_id, course.course_name, course.semester, course.academicYear, individualinfo.my_name from course, individualinfo where individualinfo.id = teacher_id and teacher_id = \'{}\' 
            '''.format(self.id)
        # 加上学期信息
        if(len(self.__semester) != 0):
            sql = sql + "and course.semester = \"{}\"".format(self.__semester)
        # 加上学年信息
        if(len(self.__academic_year) != 0):
            sql = sql + " and course.academicYear = \"{}\"".format(self.__academic_year)

        print(sql)
        try:
            self.cursor.execute(sql)
        except Exception:
            pass
        finally:
            pass
        info = self.cursor.fetchall()
        self.__set_form_course(info)
        
    # 学生成绩查询
    def query_student(self):
        self.__get_query_info()
        sql = '''select coursechoosing.id, individualinfo.my_name, course.course_id, course.course_name, coursechoosing.grade from individualinfo, course, coursechoosing where individualinfo.id = coursechoosing.id and course.course_id = coursechoosing.course_id and course.teacher_id = \'{}\'
            '''.format(self.id)
        # 加上课程号信息
        if(len(self.__course_id) != 0):
            sql = sql + "and course.course_id = \'{}\'".format(self.__course_id)
        else:
            messagebox = QMessageBox.about(self, u'提示', u'\n请加入课程号信息')
            return
        # 加上分数区间：低分
        if(len(self.__grade_low) != 0):
            sql + sql + "and coursechoosing.grade >= \'{}\'".format(self.__grade_low)
        # 加上分数去加：高分
        if(len(self.__grade_high) != 0):
            sql + sql + "and coursechoosing.grade <= \'{}\'".format(self.__grade_high)
        
        print(sql)
        try:
            self.cursor.execute(sql)
        except Exception:
            pass
        finally:
            pass
        info = self.cursor.fetchall()
        print(info)
        self.__set_form_student(info)
        
        
        pass

    # 修改学生成绩
    def modify_grade(self):
        self.__modify_dialog = modify_grade_dialog(self.id ,self.__course_id)
        self.__modify_dialog.show()
        pass

def main():
    app = QApplication(sys.argv)
    w = TeacherQueryFrame(2)
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
