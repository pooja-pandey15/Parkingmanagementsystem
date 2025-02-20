import tkinter as tk
from tkinter import messagebox, ttk
from db import initialize_db, register_user, authenticate_user, add_vehicle, exit_vehicle
from models import ParkedVehicle

class ParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking System")
        self.username = None  # Store logged-in user

        self.show_login_screen()

    def show_login_screen(self):
        """Displays the login UI."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Username:").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def login():
            if authenticate_user(username_entry.get(), password_entry.get()):
                self.username = username_entry.get()
                self.show_main_screen()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials!")

        def signup():
            if register_user(username_entry.get(), password_entry.get()):
                messagebox.showinfo("Success", "User registered!")
            else:
                messagebox.showerror("Error", "Username already exists!")

        tk.Button(self.root, text="Login", command=login).pack()
        tk.Button(self.root, text="Sign Up", command=signup).pack()

    def show_main_screen(self):
        """Displays the main parking management UI."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Welcome, {self.username}!").pack()

        # Parking Entry Section
        tk.Label(self.root, text="Plate Number:").pack()
        plate_entry = tk.Entry(self.root)
        plate_entry.pack()

        tk.Label(self.root, text="Vehicle Type (car/bike):").pack()
        type_entry = tk.Entry(self.root)
        type_entry.pack()

        def park_vehicle():
            vehicle = ParkedVehicle(plate_entry.get(), type_entry.get())
            if vehicle.park():
                messagebox.showinfo("Success", "Vehicle Parked!")
            else:
                messagebox.showerror("Error", "Duplicate Plate Number!")

        def exit_vehicle_handler():
            fare = exit_vehicle(plate_entry.get())
            if fare is not None:
                messagebox.showinfo("Success", f"Vehicle Exited! Fare: ${fare}")
            else:
                messagebox.showerror("Error", "Vehicle Not Found!")

        tk.Button(self.root, text="Park Vehicle", command=park_vehicle).pack()
        tk.Button(self.root, text="Exit Vehicle", command=exit_vehicle_handler).pack()

# Run Application
if __name__ == "__main__":
    initialize_db()
    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()
