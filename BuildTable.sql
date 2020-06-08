Create Database StudentGradeManagement default character set = utf8mb4;
USE StudentGradeManagement;

create table loginInfo
(id 		CHAR(10)	NOT NULL,
pswd		varchar(20) NOT NULL DEFAULT '123456',
flag 		char(20) NOT NULL,
CHECK(flag='学生' or flag='教师' or flag='管理员') ,
PRIMARY KEY(id)
);

create table individualInfo
(id 			CHAR(10)    NOT NULL,
my_name		CHAR(30)	DEFAULT '',
sex			CHAR(4)		DEFAULT '未定',
birth		date, /*1000-01-01*/
nation		CHAR(8),/*民族*/
major		CHAR(30),/*专业*/
station		CHAR(20),/*岗位*/
QQ			CHAR(15),
weChat		CHAR(30),
location	CHAR(100),
title		CHAR(20), /*头衔*/
CHECK(sex='男' or sex = '女' or sex = '未定'),
FOREIGN KEY(id) REFERENCES loginInfo(id),
PRIMARY KEY(id)
);

create table course
(course_id		CHAR(20) NOT NULL,
course_name		CHAR(30) NOT NULL,
semester		CHAR(10) NOT NULL,
academicYear	CHAR(4) NOT NULL,
PRIMARY KEY(course_id)
);

create table courseChoosing
(id 			CHAR(10) NOT NULL,		
course_id		CHAR(20) NOT NULL,
grade			int, 
CHECK(grade = NULL or grade > 0 and grade < 100),
PRIMARY KEY(id, course_id),
FOREIGN KEY(id) REFERENCES loginInfo(id),
FOREIGN KEY(course_id) REFERENCES course(course_id)
);
