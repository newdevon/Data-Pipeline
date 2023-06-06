from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from sqlalchemy import desc, or_
from flask_login import login_user, login_manager, current_user, LoginManager, login_required
from model import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product_retail.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

#LANDING PAGE (reroutes to dashboard)

@app.route('/')
def redirect():
    return app.redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

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
        return app.redirect(url_for('delete_teacher_error'))

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
        return app.redirect(url_for('delete_admin_error'))

    # Delete the admin from the database
    db.session.delete(admin)
    db.session.commit()

    success_message = request.form.get('success_message')
    return render_template('admin_deleted.html', success_message=success_message)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)