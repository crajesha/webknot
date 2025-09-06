import sqlite3
import random
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_NAME = 'events.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS events')
    cursor.execute('DROP TABLE IF EXISTS students')
    cursor.execute('DROP TABLE IF EXISTS registrations')
    cursor.execute('DROP TABLE IF EXISTS attendance')
    cursor.execute('DROP TABLE IF EXISTS feedback')
    cursor.execute('''
        CREATE TABLE events (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            college_id INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            college_id INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE registrations (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            UNIQUE(student_id, event_id),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE attendance (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            UNIQUE(student_id, event_id),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE feedback (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
            UNIQUE(student_id, event_id),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
    ''')
    conn.commit()
    conn.close()

def populate_mock_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    colleges = 5
    students_per_college = 500
    events_per_college = 20

    for c in range(1, colleges + 1):
        for e in range(1, events_per_college + 1):
            event_name = f'Event_{c}_{e}'
            cursor.execute('INSERT INTO events (name, college_id) VALUES (?, ?)', (event_name, c))

        for s in range(1, students_per_college + 1):
            student_name = f'Student_{c}_{s}'
            cursor.execute('INSERT INTO students (name, college_id) VALUES (?, ?)', (student_name, c))

    conn.commit()
    conn.close()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    student_id = data.get('student_id')
    event_id = data.get('event_id')
    if not student_id or not event_id:
        return jsonify({'error': 'Missing student_id or event_id'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO registrations (student_id, event_id) VALUES (?, ?)', (student_id, event_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Registration successful'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Student is already registered for this event.'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    student_id = data.get('student_id')
    event_id = data.get('event_id')
    if not student_id or not event_id:
        return jsonify({'error': 'Missing student_id or event_id'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO attendance (student_id, event_id) VALUES (?, ?)', (student_id, event_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Attendance marked successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Attendance is already marked for this student and event.'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/feedback', methods=['POST'])
def collect_feedback():
    data = request.json
    student_id = data.get('student_id')
    event_id = data.get('event_id')
    rating = data.get('rating')
    if not all([student_id, event_id, rating]):
        return jsonify({'error': 'Missing student_id, event_id, or rating'}), 400
    if not (1 <= rating <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5.'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO feedback (student_id, event_id, rating) VALUES (?, ?, ?)', (student_id, event_id, rating))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Feedback submitted successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Feedback already submitted for this student and event.'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reports/registrations')
def get_registrations_report():
    conn = get_db_connection()
    report = conn.execute('''
        SELECT e.id, e.name, COUNT(r.id) as total_registrations
        FROM events e
        LEFT JOIN registrations r ON e.id = r.event_id
        GROUP BY e.id, e.name
    ''').fetchall()
    conn.close()
    return jsonify([dict(row) for row in report])

@app.route('/reports/attendance_rate')
def get_attendance_rate_report():
    conn = get_db_connection()
    report = conn.execute('''
        SELECT 
            e.id, 
            e.name, 
            CAST(COUNT(a.id) AS REAL) * 100 / MAX(1, COUNT(r.id)) AS attendance_rate_percent
        FROM events e
        LEFT JOIN registrations r ON e.id = r.event_id
        LEFT JOIN attendance a ON e.id = a.event_id AND a.student_id = r.student_id
        GROUP BY e.id, e.name
    ''').fetchall()
    conn.close()
    return jsonify([dict(row) for row in report])

@app.route('/reports/feedback_score')
def get_feedback_score_report():
    conn = get_db_connection()
    report = conn.execute('''
        SELECT e.id, e.name, AVG(f.rating) as average_feedback
        FROM events e
        LEFT JOIN feedback f ON e.id = f.event_id
        GROUP BY e.id, e.name
    ''').fetchall()
    conn.close()
    return jsonify([dict(row) for row in report])

if __name__ == '__main__':
    setup_database()
    populate_mock_data()
    app.run(debug=True)