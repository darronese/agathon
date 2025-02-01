import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Snowpack Prediction")  # Set window title
root.geometry("400x300")  # Set window size (width x height)

# Create frame
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Run the application
root.mainloop()
