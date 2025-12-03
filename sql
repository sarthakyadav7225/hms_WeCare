-- Create Database
CREATE DATABASE IF NOT EXISTS wecare_hms;
USE wecare_hms;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Patient History Table
CREATE TABLE IF NOT EXISTS patient_history (
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
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Appointments Table
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    appointment_date VARCHAR(50) NOT NULL,
    appointment_time VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    admin_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed Default Users
-- Admin: admin@wecare.com / admin123 (SHA256 hash)
-- User: user@wecare.com / user123 (SHA256 hash)

INSERT INTO users (email, password, full_name, role, phone) VALUES
('admin@wecare.com', '8cb2237d4dd8218470424d6460e6722875db547507cb08e04cfbf2f8ab80c47', 'Admin User', 'admin', ''),
('user@wecare.com', 'd6d2897913975d68bcc2e38a97e03fc721c4f85ce1e12519e27002ba5e589bd3', 'Test User', 'user', '');

-- Verify Data
SELECT * FROM users;
