import tkinter as tk
from tkinter import ttk, messagebox
import db

# Simulated user database (Replace this with actual database logic)
USER_CREDENTIALS = {}

# Function to handle user signup
def signup():
    """Create a new user account."""
    username = entry_signup_username.get().strip()
    password = entry_signup_password.get().strip()

    if not username or not password:
        messagebox.showerror("Signup Error", "Username and Password cannot be empty!")
        return

    if username in USER_CREDENTIALS:
        messagebox.showerror("Signup Error", "Username already exists!")
        return

    USER_CREDENTIALS[username] = password
    messagebox.showinfo("Signup Successful", "You can now log in!")
    signup_window.destroy()

# Function to handle user login
def login():
    """Authenticate user and open the parking system if valid."""
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        messagebox.showinfo("Login Successful", "Welcome to Parking Management System!")
        login_window.destroy()  # Close login window
        open_parking_system()  # Open main parking system
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")

# Function to open the signup window
def open_signup_window():
    """Display the signup window for new users."""
    global signup_window, entry_signup_username, entry_signup_password

    signup_window = tk.Toplevel(login_window)
    signup_window.title("Signup")
    signup_window.geometry("300x200")

    ttk.Label(signup_window, text="New Username:").pack(pady=5)
    entry_signup_username = ttk.Entry(signup_window)
    entry_signup_username.pack(pady=5)

    ttk.Label(signup_window, text="New Password:").pack(pady=5)
    entry_signup_password = ttk.Entry(signup_window, show="*")
    entry_signup_password.pack(pady=5)

    ttk.Button(signup_window, text="Sign Up", command=signup).pack(pady=10)

# Function to open the Parking Management System
def open_parking_system():
    """Open the Parking Management System after login."""
    root = tk.Tk()
    root.title("Parking Management System")
    root.geometry("650x450")

    # Styling
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12))
    style.configure("TLabel", font=("Arial", 12))
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    # Add Vehicle Function
    def add_vehicle():
        vehicle_type = vehicle_type_var.get()
        plate_number = entry_plate.get().strip()

        if not plate_number:
            messagebox.showerror("Error", "Plate Number cannot be empty!")
            return
        
        try:
            db.add_vehicle(vehicle_type, plate_number)
            messagebox.showinfo("Success", "Vehicle Added Successfully!")
            update_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add vehicle: {e}")

    # Exit Vehicle Function
    def exit_vehicle():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a vehicle to exit!")
            return

        plate_number = tree.item(selected_item[0])['values'][1]  # Plate Number column
        db.exit_vehicle(plate_number)
        messagebox.showinfo("Success", "Vehicle Exited Successfully!")
        update_list()

    # Update List Function
    def update_list():
        """Refresh Treeview with current database data."""
        for row in tree.get_children():
            tree.delete(row)
        
        vehicles = db.get_all_vehicles()
        for vehicle in vehicles:
            tree.insert("", "end", values=vehicle)

    # GUI Layout
    frame_top = ttk.Frame(root, padding=10)
    frame_top.pack(fill="x")

    ttk.Label(frame_top, text="Vehicle Type:").pack(side="left", padx=5)
    vehicle_type_var = ttk.Combobox(frame_top, values=["Car", "Motorcycle"], state="readonly")
    vehicle_type_var.pack(side="left", padx=5)
    vehicle_type_var.current(0)

    ttk.Label(frame_top, text="Plate Number:").pack(side="left", padx=5)
    entry_plate = ttk.Entry(frame_top)
    entry_plate.pack(side="left", padx=5)

    ttk.Button(frame_top, text="Add Vehicle", command=add_vehicle).pack(side="left", padx=5)

    frame_table = ttk.Frame(root, padding=10)
    frame_table.pack(fill="both", expand=True)

    columns = ("ID", "Type", "Plate", "Entry Time", "Exit Time", "Fare")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(fill="both", expand=True)

    ttk.Button(root, text="Exit Vehicle", command=exit_vehicle).pack(pady=5)

    update_list()
    root.mainloop()

# Login Window
login_window = tk.Tk()
login_window.title("Login System")
login_window.geometry("300x250")

ttk.Label(login_window, text="Username:").pack(pady=5)
entry_username = ttk.Entry(login_window)
entry_username.pack(pady=5)

ttk.Label(login_window, text="Password:").pack(pady=5)
entry_password = ttk.Entry(login_window, show="*")
entry_password.pack(pady=5)

ttk.Button(login_window, text="Login", command=login).pack(pady=5)
ttk.Button(login_window, text="Sign Up", command=open_signup_window).pack(pady=5)

login_window.mainloop()
