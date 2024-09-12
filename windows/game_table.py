import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import random
import string

def create_editable_grid():
    # Create a new window for the game
    game_window = tk.Tk()
    game_window.title("Editable Anime Table")
    game_window.configure(bg='#1e1e1e')  # Dark background for game window
    
    # Define the table structure (headers and empty rows)
    headers = ['Anime Show', 'Anime Character', 'Anime Movie', 'Anime Power', 'Anime Weapon', 
               'Anime Place/Realm', 'Anime Studio/Author', 'Anime Monster/Race', 'Points (Value)']
    
    num_rows = 10  # Reduced number of rows to make it cleaner
    num_cols = len(headers)

    # Countdown timer function (in seconds)
    def countdown(time_left):
        minutes, seconds = divmod(time_left, 60)
        timer_label.config(text=f"Time Left: {minutes:02}:{seconds:02}")
        
        if time_left > 0:
            game_window.after(1000, countdown, time_left - 1)  # Call countdown every second
        else:
            end_game()

    # Disable all entry widgets to stop the game
    def end_game():
        for row in cells:
            for cell in row:
                cell.config(state='disabled')  # Disable all cells after time is up
        messagebox.showinfo("Game Over", "Time's up! The game has ended.")
    
    # Enable the first row for editing after the game starts
    def enable_first_row():
        for col, header in enumerate(headers):
            if header != "Points (Value)":  # Keep the "Points" column disabled
                cells[0][col].config(state='normal')  # Enable the first row (row 2 in grid)

    # Start the game and timer when the button is pressed
    def start_game():
        if random_letter_label.cget("text") == "Random Letter: ":  # If no letter is chosen
            messagebox.showerror("Error", "Please generate a random letter before starting the game.")
            return
        
        start_button.config(state='disabled')  # Disable start button after starting
        random_letter_button.config(state='disabled')  # Disable random letter generator when the game starts
        enable_first_row()  # Make the first empty row editable

        # Now start the countdown with the latest `selected_time_in_seconds`
        countdown(selected_time_in_seconds)

    # Random letter generator
    def generate_random_letter():
        letter = random.choice(string.ascii_uppercase)  # Randomly select a letter from A-Z
        random_letter_label.config(text=f"Random Letter: {letter}")  # Update label with the random letter
        start_button.config(state='normal')  # Enable the start button after a letter is chosen

    # Function to select custom time
    def ask_for_custom_time():
        custom_time = simpledialog.askinteger("Custom Time", "Enter time in minutes (1-60):", minvalue=1, maxvalue=60)
        if custom_time:
            return custom_time * 60  # Convert minutes to seconds
        return None

    # Handle time selection (Move this above its first use)
    def set_time(event):
        global selected_time_in_seconds
        selected_option = time_control_var.get()
        if selected_option == "Custom":
            custom_time = ask_for_custom_time()
            if custom_time:
                selected_time_in_seconds = custom_time  # Update with the custom time in seconds
                minutes, seconds = divmod(selected_time_in_seconds, 60)
                timer_label.config(text=f"Time Left: {minutes:02}:00")  # Update label with the custom time
        else:
            time_in_minutes = int(selected_option.split()[0])  # Get the numeric part from the option
            selected_time_in_seconds = time_in_minutes * 60  # Convert to seconds
            timer_label.config(text=f"Time Left: {time_in_minutes:02}:00")  # Update label with the selected time

    # Time control and timer in one row, centered above the table
    time_controls_frame = tk.Frame(game_window, bg='#1e1e1e')
    time_controls_frame.grid(row=0, column=1, columnspan=num_cols, pady=10)

    # Create a label for the timer inside the frame
    timer_label = tk.Label(time_controls_frame, text="Time Left: 4:00", font=('Helvetica', 16), bg='#1e1e1e', fg='white')
    timer_label.pack(side=tk.RIGHT, padx=10)

    # Time control selection dropdown inside the frame
    time_control_var = tk.StringVar(value="4 minutes")
    time_options = ["2 minutes", "4 minutes", "5 minutes", "8 minutes", "10 minutes", "Custom"]
    time_control_menu = tk.OptionMenu(time_controls_frame, time_control_var, *time_options, command=set_time)
    time_control_menu.config(font=('Helvetica', 14), bg='#61afef', fg='white')
    time_control_menu.pack(side=tk.LEFT, padx=10)

    # Create small margins on the left and right side
    left_margin = tk.Label(game_window, width=3, bg='#1e1e1e')  # Left margin
    left_margin.grid(row=1, column=0, rowspan=num_rows + 5)  # Make the margin span across the whole grid

    right_margin = tk.Label(game_window, width=3, bg='#1e1e1e')  # Right margin
    right_margin.grid(row=1, column=num_cols + 2, rowspan=num_rows + 5)  # Place the margin on the right side of the grid

    # Create header labels with styling
    for col, header in enumerate(headers):
        # Check if it's the "Points (Value)" column
        if header == "Points (Value)":
            width = 8  # Narrow width for points column
        else:
            width = 15  # Regular width for other columns

        # Allow wrapping of the header text into two lines
        header_label = tk.Label(game_window, text=header, bg="#61afef", fg="white", width=width, height=3, font=('Helvetica', 12, 'bold'), wraplength=100)
        header_label.grid(row=1, column=col + 1, sticky='nsew', padx=1, pady=1)  # Column shift for margins
    
    # Create the grid of Entry widgets (fields are now double in height)
    cells = []
    for row in range(2, num_rows + 2):  # Start from row 2 because row 1 is for headers
        row_cells = []
        for col, header in enumerate(headers):
            if header == "Points (Value)":
                width = 8  # Narrow width for points column
                state = 'disabled'  # Disable the Points column
            else:
                width = 14  # Regular width for other columns
                state = 'disabled'  # Initially, all rows are uneditable

            cell = tk.Entry(game_window, width=width, font=('Helvetica', 12), justify='center', state=state)
            cell.grid(row=row, column=col + 1, sticky='nsew', padx=1, pady=1, ipady=8)  # Column shift for margins
            row_cells.append(cell)
        cells.append(row_cells)
    
    # Make cells expand and fill space equally
    for i in range(1, num_cols + 1):  # Adjusted range for the shifted columns
        game_window.grid_columnconfigure(i, weight=1)
    for i in range(num_rows + 2):  # Adjust for header and timer
        game_window.grid_rowconfigure(i, weight=1)

    # Set default selected time to 4 minutes
    selected_time_in_seconds = 4 * 60

    # Create a start button with styling (disabled until a letter is chosen)
    start_button = tk.Button(game_window, text="Start Game", command=start_game, font=('Helvetica', 16, 'bold'), bg='green', fg='white', width=20, height=2, state='disabled')
    start_button.grid(row=num_rows + 2, column=1, columnspan=(num_cols//2), pady=10)
    
    # Create a button to generate random letter
    random_letter_button = tk.Button(game_window, text="Generate Random Letter", command=generate_random_letter, font=('Helvetica', 16, 'bold'), bg='#e06c75', fg='white', width=20, height=2)
    random_letter_button.grid(row=num_rows + 2, column=(num_cols//2 + 1), columnspan=(num_cols//2), pady=10)

    # Display label for showing random letter
    random_letter_label = tk.Label(game_window, text="Random Letter: ", font=('Helvetica', 16, 'bold'), bg='#1e1e1e', fg='white')
    random_letter_label.grid(row=num_rows + 3, column=1, columnspan=num_cols, pady=10)

    # Run the application
    game_window.mainloop()

create_editable_grid()