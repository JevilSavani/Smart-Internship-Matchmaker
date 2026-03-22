from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.db_connection import get_db_connection
from model.matcher import rank_internships

student_bp = Blueprint('student', __name__)

@student_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        skills = request.form['skills']
        location = request.form['location']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Simple validation: Check if email exists
        cursor.execute("SELECT id FROM students WHERE email = ?", (email,))
        if cursor.fetchone() is not None:
            flash("Email is already registered. Please login.", "danger")
            return redirect(url_for('student.register'))
            
        cursor.execute(
            "INSERT INTO students (name, email, password, skills, preferred_location) VALUES (?, ?, ?, ?, ?)",
            (name, email, password, skills, location) # Use hashed passwords in production!
        )
        conn.commit()
        conn.close()
        
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('student.login'))
        
    return render_template('register.html')

@student_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        student = cursor.execute(
            "SELECT * FROM students WHERE email = ? AND password = ?", (email, password)
        ).fetchone()
        
        conn.close()
        
        if student:
            session['student_id'] = student['id']
            session['student_name'] = student['name']
            return redirect(url_for('student.dashboard'))
        else:
            flash("Invalid email or password.", "danger")
            
    return render_template('login.html')

@student_bp.route('/logout')
def logout():
    session.pop('student_id', None)
    session.pop('student_name', None)
    return redirect(url_for('index'))

@student_bp.route('/dashboard')
def dashboard():
    if 'student_id' not in session:
        return redirect(url_for('student.login'))
        
    student_id = session['student_id']
    
    conn = get_db_connection()
    student = conn.cursor().execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    
    # Get all internships as dicts to avoid SQLite Row get() attribute error
    internships = [dict(row) for row in conn.cursor().execute("SELECT * FROM internships").fetchall()]
    conn.close()
    
    # Process models
    student_profile = {
        'skills': student['skills'],
        'preferred_location': student['preferred_location']
    }
    
    # Use ML model to rank internships
    ranked_internships = rank_internships(student_profile, internships)
    
    # Get top 20 recommendations
    top_internships = ranked_internships[:20]
    
    return render_template('dashboard.html', student=student, internships=top_internships)
