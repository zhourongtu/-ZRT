import sys
import mysql.connector
import mysql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import datetime

class modify_grade_dialog(QDialog):
    def __init__(self, teacher_id, course_id):
        super(modify_grade_dialog, self).__init__()

        self.conn = mysql.connector.connect(user = 'root', password = '123456', database = 'studentgrademanagement', use_unicode=True)
        self.cursor = self.conn.cursor()

        # 修改按钮
        self.__modify_btn = None
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.init__modify_grade_dialog()
    
    def init__modify_grade_dialog(self):
        self.layout = QVBoxLayout()
        self.HLayout = QHBoxLayout()

        # 课程号，学生学号，分数：标签 + 输入框。 + 按钮
        self.__course_id_label = QLabel("课程号：")
        self.__course_id_edit_line = QLineEdit()
        self.__student_id_label = QLabel("学号：")
        self.__student_id_edit_line = QLineEdit()
        self.__grade_label = QLabel("成绩：")
        self.__grade_edit_line = QLineEdit()
        self.__modify_btn = QPushButton("修改")
        self.__modify_btn.clicked.connect(self.modify)
        self.HLayout.addWidget(self.__course_id_label)
        self.HLayout.addWidget(self.__course_id_edit_line)
        self.HLayout.addWidget(self.__student_id_label)
        self.HLayout.addWidget(self.__student_id_edit_line)
        self.HLayout.addWidget(self.__grade_label)
        self.HLayout.addWidget(self.__grade_edit_line)
        self.HLayout.addWidget(self.__modify_btn)

        # 布局
        self.layout.addLayout(self.HLayout)
        self.setLayout(self.layout)

    # 修改学生成绩
    def modify(self):
        self.__course_id = self.__course_id_edit_line.text()
        self.__student_id = self.__student_id_edit_line.text()
        self.__grade = self.__grade_edit_line.text()
        
        # 先判断合法性： 查询教师是不是这门课程的老师
        sql = "select teacher_id from course where course_id = {};".format(self.__course_id)
        print(sql)
        try:
            self.cursor.execute(sql)
            temp = self.cursor.fetchall()
            print(temp[0][0])
            if(temp[0][0] != str(self.teacher_id)): # 一定要字符串化
                print(self.teacher_id)
                messagebox = QMessageBox.about(self, u'提示', u'\n修改成绩失败，你不具有权限')
        except Exception:
            messagebox = QMessageBox.about(self, u'提示', u'\n修改成绩失败,查询权限时出了问题')
            return
        finally:
            pass
        print(sql)
        
        if(str.isdigit(self.__grade) == 0):
            messagebox = QMessageBox.about(self, u'提示', u'\n分数只能为数字')
            return
        elif(int(self.__grade) < 0 or int(self.__grade) > 100):
            messagebox = QMessageBox.about(self, u'提示', u'\n分数只能只能在0~100区间内')
            return 
        # set SQL_SAFE_UPDATES = 0;
        # 可能由于安全模式的原因，导致失败
        # update coursechoosing set grade = 100 where id = 1 and course_id = 1;
        sql = "update coursechoosing set grade = {} where id = {} and course_id = {}".format(self.__grade, self.__student_id, self.__course_id)

        try:
            self.cursor.execute(sql)
            messagebox = QMessageBox.about(self, u'提示', u'\n修改成绩成功')
        except Exception:
            messagebox = QMessageBox.about(self, u'提示', u'\n修改成绩失败')
        finally:
            pass
        return
def main():
    app = QApplication(sys.argv)
    w = modify_grade_dialog(2, 1)
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()