from db import initialize_db
from ui import ParkingApp
import tkinter as tk

if __name__ == "__main__":
    initialize_db()  # Ensure database setup
    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()
