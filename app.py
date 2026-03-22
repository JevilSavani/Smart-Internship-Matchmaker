from flask import Flask, render_template, session, redirect, url_for
import os
from routes.student import student_bp
from routes.internship import internship_bp

app = Flask(__name__)
# Set a secret key for session management
app.secret_key = os.urandom(24)

# Register Blueprints
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(internship_bp, url_prefix='/internship')

@app.route('/')
def index():
    if 'student_id' in session:
        return redirect(url_for('student.dashboard'))
    return render_template('index.html')

if __name__ == '__main__':
    # Initialize DB (creates file if not exists)
    from database.db_connection import init_db
    init_db()
    app.run(debug=True)
