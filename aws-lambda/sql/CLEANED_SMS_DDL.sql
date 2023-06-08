DROP DATABASE IF EXISTS school;

CREATE DATABASE school;

USE school;

-- CREATE Tables --

CREATE TABLE student 
(
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(50)
);

CREATE TABLE teacher
(
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(50)
);

CREATE TABLE admin 
(
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(50)
);

CREATE TABLE course 
(
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(50),
    subject varchar(50),
    teacher_id int NOT NULL,
    FOREIGN KEY (teacher_id)
		REFERENCES teacher (id)
);

CREATE TABLE grade 
(
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    student_id int NOT NULL,
    course_id int NOT NULL,
    num_val int NOT NULL,
    FOREIGN KEY (student_id)
		REFERENCES student (id),
	FOREIGN KEY (course_id)
		REFERENCES course (id)
);