from flask import Blueprint, render_template, request, jsonify
from database.db_connection import get_db_connection

internship_bp = Blueprint('internship', __name__)

@internship_bp.route('/')
def list_internships():
    """ 
    Optional endpoint to just list all internships with basic pagination or filtering 
    Without ML matching.
    """
    conn = get_db_connection()
    internships = conn.cursor().execute("SELECT * FROM internships LIMIT 50").fetchall()
    conn.close()
    
    # We can create an internships_list.html template if needed, 
    # but initially we'll return a simple json API for flexibility or render a page
    return jsonify([dict(row) for row in internships])
