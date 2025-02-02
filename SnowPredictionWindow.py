if __name__ == "__main__":
    import os
    from pathlib import Path
    import matplotlib.pyplot as plt
    from tkinter import Tk, Canvas, Button, PhotoImage, Entry, Label, Spinbox, StringVar
    from tkinter import filedialog
    from tkinter import messagebox
    from buttonFunction import open_file_dialog, continue_button_action

    # Get the current directory where the script is located
    OUTPUT_PATH = Path(__file__).parent
    OUTPUT_CSV_PATH = OUTPUT_PATH / "output_csv"  # Directory containing the CSV files

    # Define the relative assets path
    ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

    # Function to clear the output directory
    def clear_output_directory(directory_path):
        try:
            # List all files in the directory
            files_in_directory = os.listdir(directory_path)
            
            # Loop through each file and remove it
            for file_name in files_in_directory:
                file_path = os.path.join(directory_path, file_name)
                
                # Check if it's a file (not a directory) before attempting to remove it
                if os.path.isfile(file_path):
                    os.remove(file_path)
            
            print(f"All files in '{directory_path}' have been deleted.")
        except Exception as e:
            print(f"Error clearing the output directory: {e}")

    # Call the function to clear the output directory when the program starts
    clear_output_directory(OUTPUT_CSV_PATH)

    # Tkinter window setup code here
    window = Tk()
    window.geometry("866x537")
    window.resizable(False, False)
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
    image_image_1 = PhotoImage(file=ASSETS_PATH/"image_1.png")
    image_1 = canvas.create_image(240.0, 250.0, image=image_image_1)

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
        text="Select CSV File",
        font=("Arial", 14),
        bg="#D9D9D9",
        wraplength=177,
        relief="flat",
        height=3,
        width=20
    )

    # Set the button size to be exactly the size of the image
    fileSelector.place(
        x=240.0 - image_width / 2,
        y=250.0 - image_height / 2,
        width=image_width,
        height=image_height
    )

    # Add the Continue button (initially hidden)
    continue_button = Button(
        window,
        text="Continue",
        font=("Arial", 14),
        bg="#D9D9D9",
        relief="flat",
        height=2,
        width=20
    )
    continue_button.place_forget()

    # Latitude Entry
    latitude_label = Label(window, text="Latitude:", font=("Arial", 12))
    latitude_label.place(x=650, y=100)

    # Use StringVar to track the latitude input
    latitude_var = StringVar()
    latitude_entry = Entry(window, textvariable=latitude_var, font=("Arial", 12))
    latitude_entry.place(x=650, y=130, width=180)

    # Longitude Entry
    longitude_label = Label(window, text="Longitude:", font=("Arial", 12))
    longitude_label.place(x=650, y=160)

    # Use StringVar to track the longitude input
    longitude_var = StringVar()
    longitude_entry = Entry(window, textvariable=longitude_var, font=("Arial", 12))
    longitude_entry.place(x=650, y=190, width=180)

    # Year Selector (Using Spinbox for year selection)
    year_label = Label(window, text="Select Year:", font=("Arial", 12))
    year_label.place(x=650, y=220)

    # Use StringVar to track the year selection
    year_var = StringVar()
    year_selector = Spinbox(window, from_=1990, to=2100, textvariable=year_var, width=10, font=("Arial", 12))
    year_selector.place(x=650, y=250)

    # Fetch and plot data function
    def updateVars():
        """Wrapper function to fetch based on user inputs."""
        global latitude, longitude, date
        # Update the global variables with the current values from the input fields
        latitude = latitude_var.get()
        longitude = longitude_var.get()
        date = year_var.get()

    # Attach the open_file_dialog function to Button 1's command
    fileSelector.config(command=lambda: open_file_dialog(fileSelector, continue_button, image_width, image_height))

    # Attach the continue_button_action function to the Continue button
    continue_button.config(command=lambda: (updateVars(), continue_button_action(fileSelector, continue_button, image_width, image_height, latitude, longitude, date)))

    # Start the Tkinter event loop
    window
    window.mainloop()
