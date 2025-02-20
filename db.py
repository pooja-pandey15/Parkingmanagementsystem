import sqlite3
import bcrypt

DB_FILE = "parking.db"

def get_db_connection():
    """Establish and return a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")  # Enforce foreign key constraints
    return conn

def initialize_db():
    """Create necessary tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Create parking records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parking_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate_number TEXT UNIQUE NOT NULL,
            vehicle_type TEXT NOT NULL,
            entry_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            exit_time DATETIME,
            fare REAL
        )
    ''')

    conn.commit()
    conn.close()

def register_user(username, password):
    """Register a new user with hashed password."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists
    finally:
        conn.close()

def authenticate_user(username, password):
    """Verify user login credentials."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user[0]):
        return True
    return False

def add_vehicle(plate_number, vehicle_type):
    """Insert a new vehicle entry into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO parking_records (plate_number, vehicle_type) VALUES (?, ?)", (plate_number, vehicle_type))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Plate number already exists
    finally:
        conn.close()

def exit_vehicle(plate_number):
    """Calculate fare and update exit time for a vehicle."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT vehicle_type FROM parking_records WHERE plate_number = ? AND exit_time IS NULL", (plate_number,))
    record = cursor.fetchone()

    if not record:
        conn.close()
        return None  # Vehicle not found

    vehicle_type = record[0]
    fare = 5 if vehicle_type == "bike" else 10  # Example fare calculation

    cursor.execute("UPDATE parking_records SET exit_time = CURRENT_TIMESTAMP, fare = ? WHERE plate_number = ?", (fare, plate_number))
    conn.commit()
    conn.close()

    return fare
