from tkinter import *
from tkinter import ttk

# Create the main window
root = Tk()
root.title("Snowpack Prediction")  # Set window title
root.geometry("400x300")  # Set window size (width x height)

# Create frame
mainframe = ttk.Frame(root, padding = "3 3 12 12")
mainframe.gride(column=0, row=0, sticky = (N, W, E, S))
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

# Run the application
root.mainloop()
