import pymysql
import hashlib
from datetime import datetime

# MySQL Connection Config
DB_CONFIG = {
    'host': 'localhost',      # Your MySQL host
    'user': 'root',           # Your MySQL username
    'password': 'password',   # Your MySQL password
    'database': 'wecare_hms', # Database name
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_connection():
    """Get MySQL connection"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except pymysql.Error as e:
        print(f"Database connection error: {e}")
        return None

def init_database():
    """Initialize database with all required tables"""
    conn = get_connection()
    if not conn:
        print("Failed to connect to database")
        return
    
    c = conn.cursor()

    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        role VARCHAR(50) DEFAULT 'user',
        phone VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # Patient history table
    c.execute('''CREATE TABLE IF NOT EXISTS patient_history (
        patient_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        name VARCHAR(255),
        age INT,
        gender VARCHAR(50),
        disease_name VARCHAR(255),
        symptoms TEXT,
        severity_level VARCHAR(50),
        medical_history TEXT,
        diagnosis_date VARCHAR(50),
        appointment_id INT,
        appointment_date VARCHAR(50),
        appointment_time VARCHAR(50),
        status VARCHAR(50),
        visit_type VARCHAR(50),
        height_cm FLOAT,
        weight_kg FLOAT,
        BMI FLOAT,
        smoking_status VARCHAR(50),
        exercise_level VARCHAR(50),
        treatment_given TEXT,
        medicine_prescribed TEXT,
        treatment_cost FLOAT,
        follow_up_date VARCHAR(50),
        total_amount FLOAT,
        insurance_used VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        INDEX(user_id)
    )''')

    # Appointments table
    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
        appointment_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        appointment_date VARCHAR(50) NOT NULL,
        appointment_time VARCHAR(50) NOT NULL,
        status VARCHAR(50) DEFAULT 'pending',
        admin_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        INDEX(user_id)
    )''')

    conn.commit()

    # ---------- SEED DEFAULT ADMIN & USER ----------
    admin_email = "admin@wecare.com"
    user_email = "user@wecare.com"

    # Admin user
    c.execute("SELECT 1 FROM users WHERE email = %s", (admin_email,))
    if not c.fetchone():
        c.execute(
            "INSERT INTO users (email, password, full_name, role, phone) VALUES (%s, %s, %s, %s, %s)",
            (admin_email, hash_password("admin123"), "Admin User", "admin", "")
        )

    # Normal user
    c.execute("SELECT 1 FROM users WHERE email = %s", (user_email,))
    if not c.fetchone():
        c.execute(
            "INSERT INTO users (email, password, full_name, role, phone) VALUES (%s, %s, %s, %s, %s)",
            (user_email, hash_password("user123"), "Test User", "user", "")
        )

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email, password, full_name, role='user', phone=''):
    """Create new user account"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"
        
        c = conn.cursor()
        hashed_pwd = hash_password(password)
        c.execute(
            "INSERT INTO users (email, password, full_name, role, phone) VALUES (%s, %s, %s, %s, %s)",
            (email, hashed_pwd, full_name, role, phone)
        )
        conn.commit()
        conn.close()
        return True, "User created successfully"
    except pymysql.IntegrityError:
        return False, "Email already exists"
    except Exception as e:
        return False, str(e)

def get_user_by_email(email):
    """Get user by email"""
    try:
        conn = get_connection()
        if not conn:
            return None
        
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = c.fetchone()
        conn.close()
        
        if user:
            return {
                'user_id': user['user_id'],
                'email': user['email'],
                'full_name': user['full_name'],
                'role': user['role'],
                'phone': user['phone']
            }
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def verify_password(email, password):
    """Verify user password"""
    try:
        conn = get_connection()
        if not conn:
            return False
        
        c = conn.cursor()
        hashed_pwd = hash_password(password)
        c.execute('SELECT * FROM users WHERE email = %s AND password = %s',
                  (email, hashed_pwd))
        user = c.fetchone()
        conn.close()
        
        return user is not None
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_all_users():
    """Get all users (admin only)"""
    try:
        conn = get_connection()
        if not conn:
            return []
        
        c = conn.cursor()
        c.execute('SELECT user_id, email, full_name, role, phone, created_at FROM users')
        users = c.fetchall()
        conn.close()
        return users
    except Exception as e:
        print(f"Error: {e}")
        return []

def add_patient_history(user_id, patient_data):
    """Add patient history record"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"
        
        c = conn.cursor()
        c.execute('''INSERT INTO patient_history
                     (user_id, name, age, gender, disease_name, symptoms, severity_level,
                      medical_history, diagnosis_date, height_cm, weight_kg, BMI,
                      smoking_status, exercise_level, treatment_given, medicine_prescribed,
                      treatment_cost, follow_up_date, total_amount, insurance_used, status)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
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
    try:
        conn = get_connection()
        if not conn:
            return []
        
        c = conn.cursor()
        c.execute('SELECT * FROM patient_history WHERE user_id = %s ORDER BY created_at DESC', (user_id,))
        records = c.fetchall()
        conn.close()
        return records
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_all_patient_history():
    """Get all patient history (admin only)"""
    try:
        conn = get_connection()
        if not conn:
            return []
        
        c = conn.cursor()
        c.execute('SELECT * FROM patient_history ORDER BY created_at DESC')
        records = c.fetchall()
        conn.close()
        return records
    except Exception as e:
        print(f"Error: {e}")
        return []

def add_appointment(user_id, appointment_date, appointment_time):
    """Add appointment"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"
        
        c = conn.cursor()
        c.execute(
            'INSERT INTO appointments (user_id, appointment_date, appointment_time) VALUES (%s, %s, %s)',
            (user_id, appointment_date, appointment_time)
        )
        conn.commit()
        conn.close()
        return True, "Appointment scheduled successfully"
    except Exception as e:
        return False, str(e)

def get_appointments(user_id):
    """Get appointments for user"""
    try:
        conn = get_connection()
        if not conn:
            return []
        
        c = conn.cursor()
        c.execute('SELECT * FROM appointments WHERE user_id = %s ORDER BY appointment_date DESC',
                  (user_id,))
        appointments = c.fetchall()
        conn.close()
        return appointments
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_all_appointments():
    """Get all appointments (admin only)"""
    try:
        conn = get_connection()
        if not conn:
            return []
        
        c = conn.cursor()
        c.execute('SELECT * FROM appointments ORDER BY appointment_date DESC')
        appointments = c.fetchall()
        conn.close()
        return appointments
    except Exception as e:
        print(f"Error: {e}")
        return []
