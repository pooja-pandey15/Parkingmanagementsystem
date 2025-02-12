import sqlite3
from datetime import datetime

DB_FILE = "data/parking.db"

def connect_db():
    """Connect to SQLite database and create tables if not exists."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Table for parking data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_type TEXT,
            plate_number TEXT UNIQUE,
            entry_time TEXT,
            exit_time TEXT DEFAULT NULL,
            fare REAL DEFAULT 0
        )
    ''')

    # Table for users (authentication)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    return conn

def add_vehicle(vehicle_type, plate_number):
    """Adds a vehicle with automatic entry time."""
    conn = connect_db()
    cursor = conn.cursor()
    
    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute('''
            INSERT INTO parking (vehicle_type, plate_number, entry_time)
            VALUES (?, ?, ?)
        ''', (vehicle_type, plate_number, entry_time))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("Error: Vehicle with this plate number already exists.")
        return False
    finally:
        conn.close()

def exit_vehicle(plate_number):
    """Updates exit time and calculates fare."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT entry_time, vehicle_type FROM parking WHERE plate_number = ?", (plate_number,))
    result = cursor.fetchone()

    if result:
        entry_time, vehicle_type = result
        exit_time = datetime.now()
        entry_time = datetime.strptime(entry_time, "%Y-%m-%d %H:%M:%S")

        duration_hours = (exit_time - entry_time).total_seconds() / 3600
        rate_per_hour = 50 if vehicle_type.lower() == "car" else 20
        fare = round(duration_hours * rate_per_hour, 2)

        cursor.execute('''
            UPDATE parking SET exit_time = ?, fare = ? WHERE plate_number = ?
        ''', (exit_time.strftime("%Y-%m-%d %H:%M:%S"), fare, plate_number))
        
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

def get_all_vehicles():
    """Fetch all vehicles from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, vehicle_type, plate_number, entry_time, exit_time, fare FROM parking")
    data = cursor.fetchall()
    conn.close()
    return data
