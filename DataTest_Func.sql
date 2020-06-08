USE studentgrademanagement;
# 插入课程
INSERT INTO `studentgrademanagement`.`course`
(`course_id`,
`course_name`,
`semester`,
`academicYear`,
`teacher_id`)
VALUES
("1",
"C语言",
"秋冬",
"2019",
"2");

INSERT INTO course(
course_id, course_name, semester, academicYear
)
VALUES(
"1" , "C语言", "秋冬" ,"2019"
);
# 插入登录账号与密码
INSERT INTO logininfo(
id, pswd, flag
)
VALUES(
"1", "zhourongtu", "学生"
);
INSERT INTO logininfo(
id, pswd, flag
)
VALUES(
"2", "lvjiang", "老师"
);
# 插入个人信息
INSERT INTO individualinfo(
id, my_name, sex, birth, nation, major, station, QQ, weChat, location, title
)
VALUES(
"1", "周荣图", "男", "1999-6-8", "汉", "测控技术与仪器", "无", "11111111", "xxxx", "中国大陆", "在读学生"
);

# 插入选课
INSERT INTO `studentgrademanagement`.`coursechoosing`
(`id`,
`course_id`,
`grade`)
VALUES
("1",
"1",
100);


# 登录时查询
select id = "1" as "账号", pswd as "密码", flag as "身份" from logininfo;

# 信息修改时更新 
UPDATE `studentgrademanagement`.`individualinfo`
SET
`id` = "1",
`my_name` = "周荣图",
`sex` = "男",
`birth` = "1999-6-8",
`nation` = "汉",
`major` = "测控技术与仪器",
`station` = "无",
`QQ` = "11111",
`weChat` = "weixinhaoma",
`location` = "中国浙江",
`title` = "在读学生"
WHERE `id` = "1";

select * from individualinfo;

# 查询成绩，按学期+学年
select coursechoosing.course_id, course_name, grade from coursechoosing left join course on coursechoosing.course_id = course.course_id
where id = "1" AND semester = "秋冬" AND academicYear = "2019";

# 查询成绩，按课程号
select coursechoosing.course_id, course_name, grade from coursechoosing left join course on coursechoosing.course_id = course.course_id
where coursechoosing.course_id = "1" AND id = "1";

# 查询成绩， 按学年查询
select coursechoosing.course_id, course_name, grade from coursechoosing left join course on coursechoosing.course_id = course.course_id
where academicYear = "2019" AND id = "1";

# 教师查询
# 查看当前教授课程
select * from course where teacher_id = "2";
# 按照学年查看教授课程
select * from course where teacher_id = "2" AND academicYear = "2019";
# 按照学年+学期查看教授课程
select * from course where teacher_id = "2" AND academicYear = "2019" AND semester = "秋冬";
# 按课程号查看成绩
select * from coursechoosing where course_id = "1";# 教师和课程一一对应（特殊情况暂时不考虑）
# 老师按课程号+成绩段查看成绩
select * from coursechoosing where course_id = "1" AND grade <= 100 AND grade >= 60;

# 老师修改学生成绩
UPDATE `studentgrademanagement`.`coursechoosing`
SET
`grade` = 60
WHERE `id` = "1" AND `course_id` = "1";

# 其他

