from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, filedialog  # Import filedialog for file selection
import os
import pandas as pd
from separateCSV import split_data_by_coordinates  # Import the function to split CSV


# Get the current directory where the script is located
OUTPUT_PATH = Path(__file__).parent

# Define the relative assets path
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"  # Assuming the folder is in the same directory as the script


def relative_to_assets(path: str) -> Path:
    # Combine the relative path with the assets directory
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("866x537")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=537,
    width=866,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

# Use the relative path to load the image
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    240.0,
    250.0,
    image=image_image_1
)

# Retrieve the image size
image_width = image_image_1.width()
image_height = image_image_1.height()

canvas.create_text(
    40.0,
    40.0,
    anchor="nw",
    text="Snowpack Predictor",
    fill="#000000",
    font=("Ubuntu Regular", 32 * -1)
)

# Button 1 (file selection button with text instead of image)
fileSelector = Button(
    window,
    text="Select CSV File",  # Default text on the button
    font=("Arial", 14),    # Text font for the button
    bg="#D9D9D9",          # Background color to make the text visible
    wraplength=177,         # Ensures the text doesn't overflow and wraps inside the button
    relief="flat",         # Flat style to remove borders
    height=3,              # Increase the height to make it more readable
    width=20               # Adjust the width to make it look nicer
)

# Set the button size to be exactly the size of the image
fileSelector.place(
    x=240.0 - image_width / 2,  # Adjusting x position to center the button
    y=250.0 - image_height / 2,  # Adjusting y position to center the button
    width=image_width,  # Button width matches the image width
    height=image_height  # Button height matches the image height
)

# Function to open the file dialog and select a CSV file
def open_file_dialog():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")]  # Limit file selection to CSV files
    )
    
    # If a file is selected (file_path is not empty)
    if file_path:
        # Update Button 1 text with the full file path
        fileSelector.config(text=file_path)  # Button 1's text becomes the file path
        
        # Show the Continue button after file selection
        continue_button.place(
            x=240.0 - image_width / 2,  # Same X position as Button 1
            y=250.0 + image_height / 2 + 10,  # Place it just below Button 1
            width=image_width / 2 - 5,  # Button width adjusted to take half of Button 1's width
            height=50  # Adjust height to make it look nice
        )
        
        # Hide the Deselect button after file selection
        deselect_button.place_forget()

# Attach the open_file_dialog function to Button 1's command
fileSelector.config(command=open_file_dialog)

# Rectangle (existing)
canvas.create_rectangle(
    500.0,
    173.0,
    677.0,
    395.0,
    fill="#D9D9D9",
    outline=""
)

# Function for Continue button
def continue_button_action():
    # Get the selected file path
    selected_file = fileSelector.cget("text")
    
    # Check if a file is selected and it ends with ".csv"
    if selected_file and selected_file.endswith(".csv"):
        # Call the split_data_by_coordinates function for CSV file separation
        split_data_by_coordinates(selected_file)  # Only separate the CSV file
        
        # Hide Button 1 (File Selector button)
        fileSelector.place_forget()
        
        # Hide the Continue button
        continue_button.place_forget()

        # Show the Deselect button after pressing Continue
        deselect_button.place(
            x=240.0 - image_width / 2,  # Same X position as Button 1
            y=250.0 + image_height / 2 + 10,  # Just below Button 1
            width=image_width / 2 - 5,  # Button width adjusted to take half of Button 1's width
            height=50  # Adjust height to make it look nice
        )
    else:
        # If no file is selected or it's not a valid CSV file, show an error
        print("Please select a valid CSV file.")

# Add the Continue button (initially hidden)
continue_button = Button(
    window,
    text="Continue",  # Text on the button
    font=("Arial", 14),  # Text font for the button
    bg="#D9D9D9",  # Button background color
    relief="flat",  # Flat style to remove borders
    height=2,  # Adjust the height to make it look nicer
    width=20  # Adjust the width to make it look nicer
)
continue_button.place_forget()  # Initially hide the button

# Attach the continue_button_action function to the Continue button
continue_button.config(command=continue_button_action)

# Function for Deselect button (clear the file selection)
def deselect_file():
    # Clear the file path from Button 1
    fileSelector.place(
        x=240.0 - image_width / 2,  # Adjusting x position to center the button
        y=250.0 - image_height / 2,  # Adjusting y position to center the button
        width=image_width,  # Button width matches the image width
        height=image_height  # Button height matches the image height
    )
    fileSelector.config(text="Select CSV File")
    
    # Hide the Deselect button
    deselect_button.place_forget()

# Add the Deselect button (initially hidden)
deselect_button = Button(
    window,
    text="Deselect File",  # Text on the button
    font=("Arial", 14),  # Text font for the button
    bg="#D9D9D9",  # Button background color
    relief="flat",  # Flat style to remove borders
    height=2,  # Adjust the height to make it look nicer
    width=20  # Adjust the width to make it look nicer
)
deselect_button.place_forget()  # Initially hide the button

# Attach the deselect_file function to the Deselect button
deselect_button.config(command=deselect_file)

# Start the Tkinter event loop
window.mainloop()
