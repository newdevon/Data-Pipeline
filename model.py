from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

###  Models  ####

class Student(db.Model, UserMixin):
    __tablename__ = "student"

    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50), unique=False, nullable=False)
    student_email = db.Column(db.String(50), unique=True, nullable=False)

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def to_dict(self):
      return {
        'student name': self.student_name,
        'email': self.student_email
      }

    def get_id(self):
        return str(self.student_id)


class Teacher(db.Model):
    __tablename__ = "teacher"
    teacher_id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(50))
    teacher_email = db.Column(db.String(50))

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    
    def to_dict(self):
      return {
        'teacher name': self.teacher_name,
        'email': self.teacher_email
      }
    
    def get_id(self):
        return str(self.teacher_id)

class Grade(db.Model):
    __tablename__ = "grade"
    grade_id = db.Column(db.Integer, primary_key=True)
    num_val = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def to_dict(self):
      return {
        'numerical grade': self.num_val,
      }
    
    def get_id(self):
        return str(self.grade_id)

class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.teacher_id"))
    course_name = db.Column(db.String(50))
    subject = db.Column(db.String(50))

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    
    def to_dict(self):
      return {
        'course name' : self.course_name,
        'course subject': self.subject,
      }
    
    def get_id(self):
        return str(self.id)
    
class Administrator(db.Model):
    __tablename__ = "admin"
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(50))
    admin_email = db.Column(db.String(50))

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    
    def to_dict(self):
      return {
        'admin name': self.admin_name,
        'email': self.admin_email
      }
    
    def get_id(self):
        return str(self.admin_id)
