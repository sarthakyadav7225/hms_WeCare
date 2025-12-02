import sqlite3
import hashlib
from datetime import datetime

DB_PATH = "wecare_hms.db"

def init_database():
    """Initialize database with all required tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Patient history table
    c.execute('''CREATE TABLE IF NOT EXISTS patient_history (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT,
        age INTEGER,
        gender TEXT,
        disease_name TEXT,
        symptoms TEXT,
        severity_level TEXT,
        medical_history TEXT,
        diagnosis_date TEXT,
        appointment_id INTEGER,
        appointment_date TEXT,
        appointment_time TEXT,
        status TEXT,
        visit_type TEXT,
        height_cm REAL,
        weight_kg REAL,
        BMI REAL,
        smoking_status TEXT,
        exercise_level TEXT,
        treatment_given TEXT,
        medicine_prescribed TEXT,
        treatment_cost REAL,
        follow_up_date TEXT,
        total_amount REAL,
        insurance_used TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )''')
    
    # Appointments table
    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        admin_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email, password, full_name, role='user', phone=''):
    """Create new user account"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        hashed_pwd = hash_password(password)
        c.execute('''INSERT INTO users (email, password, full_name, role, phone)
                     VALUES (?, ?, ?, ?, ?)''',
                  (email, hashed_pwd, full_name, role, phone))
        conn.commit()
        conn.close()
        return True, "User created successfully"
    except sqlite3.IntegrityError:
        return False, "Email already exists"
    except Exception as e:
        return False, str(e)

def get_user_by_email(email):
    """Get user by email"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    if user:
        return {
            'user_id': user[0],
            'email': user[1],
            'full_name': user[3],
            'role': user[4],
            'phone': user[5]
        }
    return None

def verify_password(email, password):
    """Verify user password"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hashed_pwd = hash_password(password)
    c.execute('SELECT * FROM users WHERE email = ? AND password = ?',
              (email, hashed_pwd))
    user = c.fetchone()
    conn.close()
    return user is not None

def get_all_users():
    """Get all users (admin only)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT user_id, email, full_name, role, phone, created_at FROM users')
    users = c.fetchall()
    conn.close()
    return users

def add_patient_history(user_id, patient_data):
    """Add patient history record"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO patient_history 
                     (user_id, name, age, gender, disease_name, symptoms, severity_level,
                      medical_history, diagnosis_date, height_cm, weight_kg, BMI,
                      smoking_status, exercise_level, treatment_given, medicine_prescribed,
                      treatment_cost, follow_up_date, total_amount, insurance_used, status)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (user_id, patient_data.get('name'), patient_data.get('age'),
                   patient_data.get('gender'), patient_data.get('disease_name'),
                   patient_data.get('symptoms'), patient_data.get('severity_level'),
                   patient_data.get('medical_history'), datetime.now().strftime('%Y-%m-%d'),
                   patient_data.get('height_cm'), patient_data.get('weight_kg'),
                   patient_data.get('BMI'), patient_data.get('smoking_status'),
                   patient_data.get('exercise_level'), patient_data.get('treatment_given'),
                   patient_data.get('medicine_prescribed'), patient_data.get('treatment_cost'),
                   patient_data.get('follow_up_date'), patient_data.get('total_amount'),
                   patient_data.get('insurance_used'), 'completed'))
        conn.commit()
        conn.close()
        return True, "Patient record added successfully"
    except Exception as e:
        return False, str(e)

def get_patient_history(user_id):
    """Get patient history for specific user"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM patient_history WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    records = c.fetchall()
    conn.close()
    return records

def get_all_patient_history():
    """Get all patient history (admin only)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM patient_history ORDER BY created_at DESC')
    records = c.fetchall()
    conn.close()
    return records

def add_appointment(user_id, appointment_date, appointment_time):
    """Add appointment"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO appointments (user_id, appointment_date, appointment_time)
                     VALUES (?, ?, ?)''',
                  (user_id, appointment_date, appointment_time))
        conn.commit()
        conn.close()
        return True, "Appointment scheduled successfully"
    except Exception as e:
        return False, str(e)

def get_appointments(user_id):
    """Get appointments for user"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM appointments WHERE user_id = ? ORDER BY appointment_date DESC',
              (user_id,))
    appointments = c.fetchall()
    conn.close()
    return appointments

def get_all_appointments():
    """Get all appointments (admin only)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM appointments ORDER BY appointment_date DESC')
    appointments = c.fetchall()
    conn.close()
    return appointments
