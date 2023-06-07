from flask import Flask, request, render_template, redirect, url_for
from model import *
import csv
from io import StringIO
import sqlite3 as sq
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

#LANDING PAGE (reroutes to dashboard)

@app.route('/')
def direct_to_dashboard():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/save', methods=['GET'])
def save():
    
    conn = sq.connect('instance/school_management.db')
    sql_query = pd.read_sql_query('''
                              SELECT * FROM student
                              '''
                              ,conn) 

    df = pd.DataFrame(sql_query)
    df.to_csv (r'raw-csv-files\student.csv', index = False)

    sql_query = pd.read_sql_query('''
                              SELECT * FROM teacher
                              '''
                              ,conn) 

    df = pd.DataFrame(sql_query)
    df.to_csv (r'raw-csv-files\teacher.csv', index = False)

    sql_query = pd.read_sql_query('''
                              SELECT * FROM administrator
                              '''
                              ,conn) 

    df = pd.DataFrame(sql_query)
    df.to_csv (r'raw-csv-files\admin.csv', index = False)

    sql_query = pd.read_sql_query('''
                              SELECT * FROM grade
                              '''
                              ,conn) 

    df = pd.DataFrame(sql_query)
    df.to_csv (r'raw-csv-files\grades.csv', index = False)

    sql_query = pd.read_sql_query('''
                              SELECT * FROM class
                              '''
                              ,conn) 

    df = pd.DataFrame(sql_query)
    df.to_csv (r'raw-csv-files\course.csv', index = False)

    return render_template('files_saved.html')

#STUDENTS

#selection page
@app.route('/students')
def students():
    return render_template('students.html')

#Add
@app.route('/students/add', methods=['GET', 'POST'])
def render_add_student_form():
    if request.method == 'POST':
        return add_student()
    else:
        return render_template('add_student.html')

@app.route('/students/added', methods=['POST'])
def add_student():
    student_name = request.form['student_name']
    student_email = request.form['student_email']

    student = Student(
        
        student_name=student_name,
        student_email=student_email
    )
    db.session.add(student)
    db.session.commit()

    success_message = request.form.get('success_message')
    return render_template('student_created.html', success_message=success_message)

#Delete
@app.route('/students/delete', methods=['GET', 'POST'])
def render_delete_student_form():
    if request.method == 'POST':
        return delete_student()
    else:
        return render_template('delete_student.html')
    
@app.route('/students/delete/failed')
def delete_student_error():
    return render_template('student_deletion_failed.html')
    

@app.route('/students/deleted', methods=['DELETE', 'POST'])
def delete_student():
    # Retrieve the student ID from the request data
    student_id = request.form.get('student_id')

    # Retrieve the student from the database
    student = Student.query.get(student_id)
    if not student:
        return app.redirect(url_for('delete_student_error'))

    # Delete the student from the database
    db.session.delete(student)
    db.session.commit()

    success_message = request.form.get('success_message')
    return render_template('student_deleted.html', success_message=success_message)

#TEACHERS

#selection page
@app.route('/teachers')
def teachers():
    return render_template('teachers.html')

#Add
@app.route('/teachers/add', methods=['GET', 'POST'])
def render_add_teacher_form():
    if request.method == 'POST':
        return add_teacher()
    else:
        return render_template('add_teacher.html')

@app.route('/teachers/added', methods=['POST'])
def add_teacher():
    teacher_name = request.form['teacher_name']
    teacher_email = request.form['teacher_email']

    teacher = Teacher(
        
        teacher_name=teacher_name,
        teacher_email=teacher_email
    )
    db.session.add(teacher)
    db.session.commit()

    success_message = request.form.get('success_message')
    return render_template('teacher_created.html', success_message=success_message)

#Delete
@app.route('/teachers/delete', methods=['GET', 'POST'])
def render_delete_teacher_form():
    if request.method == 'POST':
        return delete_teacher()
    else:
        return render_template('delete_teacher.html')
    
@app.route('/teachers/delete/failed')
def delete_teacher_error():
    return render_template('teacher_deletion_failed.html')
    

@app.route('/teachers/deleted', methods=['DELETE', 'POST'])
def delete_teacher():
    # Retrieve the teacher ID from the request data
    teacher_id = request.form.get('teacher_id')

    # Retrieve the teacher from the database
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return redirect(url_for('delete_teacher_error'))

    # Delete the teacher from the database
    db.session.delete(teacher)
    db.session.commit()

    success_message = request.form.get('success_message')
    return render_template('teacher_deleted.html', success_message=success_message)

#ADMINS

#selection page
@app.route('/admins')
def admins():
    return render_template('admins.html')

#Add
@app.route('/admins/add', methods=['GET', 'POST'])
def render_add_admin_form():
    if request.method == 'POST':
        return add_admin()
    else:
        return render_template('add_admin.html')

@app.route('/admins/added', methods=['POST'])
def add_admin():
    admin_name = request.form['admin_name']
    admin_email = request.form['admin_email']

    admin = Administrator(
        
        admin_name=admin_name,
        admin_email=admin_email
    )
    db.session.add(admin)
    db.session.commit()

    success_message = request.form.get('success_message')
    return render_template('admin_created.html', success_message=success_message)

#Delete
@app.route('/admins/delete', methods=['GET', 'POST'])
def render_delete_admin_form():
    if request.method == 'POST':
        return delete_admin()
    else:
        return render_template('delete_admin.html')
    
@app.route('/admins/delete/failed')
def delete_admin_error():
    return render_template('admin_deletion_failed.html')
    

@app.route('/admins/deleted', methods=['DELETE', 'POST'])
def delete_admin():
    # Retrieve the admin ID from the request data
    admin_id = request.form.get('admin_id')

    # Retrieve the admin from the database
    admin = Administrator.query.get(admin_id)
    if not admin:
        return redirect(url_for('delete_admin_error'))

    # Delete the admin from the database
    db.session.delete(admin)
    db.session.commit()

    success_message = request.form.get('success_message')
    return render_template('admin_deleted.html', success_message=success_message)

#GRADES

#selection page
@app.route('/grades')
def grades():
    return render_template('grades.html')

#Add
@app.route('/grades/add', methods=['GET', 'POST'])
def render_add_grade_form():
    if request.method == 'POST':
        return add_grade()
    else:
        return render_template('add_grade.html')

@app.route('/grades/added', methods=['POST'])
def add_grade():
    num_val = request.form['num_val']
    student_id = request.form['student_id']
    class_id = request.form['class_id']

    grade = Grade(
        
        num_val=num_val,
        student_id=student_id,
        class_id=class_id
    )
    db.session.add(grade)
    db.session.commit()

    success_message = request.form.get('success_message')
    return render_template('grade_created.html', success_message=success_message)

#Delete
@app.route('/grades/delete', methods=['GET', 'POST'])
def render_delete_grade_form():
    if request.method == 'POST':
        return delete_grade()
    else:
        return render_template('delete_grade.html')
    
@app.route('/grades/delete/failed')
def delete_grade_error():
    return render_template('grade_deletion_failed.html')
    

@app.route('/grades/deleted', methods=['DELETE', 'POST'])
def delete_grade():
    # Retrieve the grade ID from the request data
    grade_id = request.form.get('grade_id')

    # Retrieve the grade from the database
    grade = Grade.query.get(grade_id)
    if not grade:
        return app.redirect(url_for('delete_grade_error'))

    # Delete the grade from the database
    db.session.delete(grade)
    db.session.commit()

    success_message = request.form.get('success_message')
    return render_template('grade_deleted.html', success_message=success_message)

#CLASSES

#selection page
@app.route('/courses')
def classs():
    return render_template('courses.html')

#Add
@app.route('/courses/add', methods=['GET', 'POST'])
def render_add_class_form():
    if request.method == 'POST':
        return add_class()
    else:
        return render_template('add_course.html')

@app.route('/courses/added', methods=['POST'])
def add_class():

    teacher_id = request.form['teacher_id']
    class_name = request.form['class_name']
    class_subject = request.form['class_subject']

    add_class = Class(
        
        teacher_id=teacher_id,
        class_name=class_name,
        class_subject=class_subject
    )
    db.session.add(add_class)
    db.session.commit()

    success_message = request.form.get('success_message')
    return render_template('course_created.html', success_message=success_message)

#Delete
@app.route('/courses/delete', methods=['GET', 'POST'])
def render_delete_class_form():
    if request.method == 'POST':
        return delete_class()
    else:
        return render_template('delete_course.html')
    
@app.route('/courses/delete/failed')
def delete_class_error():
    return render_template('course_deletion_failed.html')
    

@app.route('/courses/deleted', methods=['DELETE', 'POST'])
def delete_class():
    # Retrieve the class ID from the request data
    class_id = request.form.get('course_id')

    # Retrieve the class from the database
    del_class = Class.query.get(class_id)
    if not del_class:
        return app.redirect(url_for('delete_class_error'))

    # Delete the class from the database
    db.session.delete(del_class)
    db.session.commit()

    success_message = request.form.get('success_message')
    return render_template('course_deleted.html', success_message=success_message)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)



    