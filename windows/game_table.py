import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import random
import string

def create_editable_grid():
    # Function to create the game grid
    game_window = tk.Tk()
    game_window.title("Editable Anime Table")
    game_window.configure(bg='#1e1e1e')
    
    # Define the table structure
    headers = ['Anime Show', 'Anime Character', 'Anime Movie', 'Anime Power', 'Anime Weapon', 
               'Anime Place/Realm', 'Anime Studio/Author', 'Anime Monster/Race', 'Points (Value)']
    
    num_rows = 10
    num_cols = len(headers)

    def countdown(time_left):
        minutes, seconds = divmod(time_left, 60)
        timer_label.config(text=f"Time Left: {minutes:02}:{seconds:02}")
        
        if time_left > 0:
            game_window.after(1000, countdown, time_left - 1)
        else:
            end_game()

    def end_game():
        for row in cells:
            for cell in row:
                cell.config(state='disabled')
        messagebox.showinfo("Game Over", "Time's up! The game has ended.")
    
    def enable_first_row():
        for col, header in enumerate(headers):
            if header != "Points (Value)":
                cells[0][col].config(state='normal')

    def start_game():
        global selected_time_in_seconds
        if random_letter_label.cget("text") == "Random Letter: ":
            messagebox.showerror("Error", "Please generate a random letter before starting the game.")
            return
        
        start_button.config(state='disabled')
        random_letter_button.config(state='disabled')
        enable_first_row()

        countdown(selected_time_in_seconds)

    def generate_random_letter():
        letter = random.choice(string.ascii_uppercase)
        random_letter_label.config(text=f"Random Letter: {letter}")
        start_button.config(state='normal')

    def ask_for_custom_time():
        custom_time = simpledialog.askinteger("Custom Time", "Enter time in minutes (1-60):", minvalue=1, maxvalue=60)
        if custom_time:
            return custom_time * 60
        return None

    def set_time(event=None):
        global selected_time_in_seconds
        selected_option = time_control_var.get()
        if selected_option == "Custom":
            custom_time = ask_for_custom_time()
            if custom_time:
                selected_time_in_seconds = custom_time
                minutes, seconds = divmod(selected_time_in_seconds, 60)
                timer_label.config(text=f"Time Left: {minutes:02}:00")
        else:
            time_in_minutes = int(selected_option.split()[0])
            selected_time_in_seconds = time_in_minutes * 60
            timer_label.config(text=f"Time Left: {time_in_minutes:02}:00")

    time_controls_frame = tk.Frame(game_window, bg='#1e1e1e')
    time_controls_frame.grid(row=0, column=1, columnspan=num_cols, pady=10)

    timer_label = tk.Label(time_controls_frame, text="Time Left: 4:00", font=('Helvetica', 16), bg='#1e1e1e', fg='white')
    timer_label.pack(side=tk.RIGHT, padx=10)

    time_control_var = tk.StringVar(value="4 minutes")
    time_options = ["2 minutes", "4 minutes", "5 minutes", "8 minutes", "10 minutes", "Custom"]
    time_control_menu = tk.OptionMenu(time_controls_frame, time_control_var, *time_options, command=set_time)
    time_control_menu.config(font=('Helvetica', 14), bg='#61afef', fg='white')
    time_control_menu.pack(side=tk.LEFT, padx=10)

    left_margin = tk.Label(game_window, width=3, bg='#1e1e1e')
    left_margin.grid(row=1, column=0, rowspan=num_rows + 5)

    right_margin = tk.Label(game_window, width=3, bg='#1e1e1e')
    right_margin.grid(row=1, column=num_cols + 2, rowspan=num_rows + 5)

    for col, header in enumerate(headers):
        if header == "Points (Value)":
            width = 8
        else:
            width = 15

        header_label = tk.Label(game_window, text=header, bg="#61afef", fg="white", width=width, height=3, font=('Helvetica', 12, 'bold'), wraplength=100)
        header_label.grid(row=1, column=col + 1, sticky='nsew', padx=1, pady=1)
    
    cells = []
    for row in range(2, num_rows + 2):
        row_cells = []
        for col, header in enumerate(headers):
            if header == "Points (Value)":
                width = 8
                state = 'disabled'
            else:
                width = 14
                state = 'disabled'

            cell = tk.Entry(game_window, width=width, font=('Helvetica', 12), justify='center', state=state)
            cell.grid(row=row, column=col + 1, sticky='nsew', padx=1, pady=1, ipady=8)
            row_cells.append(cell)
        cells.append(row_cells)
    
    for i in range(1, num_cols + 1):
        game_window.grid_columnconfigure(i, weight=1)
    for i in range(num_rows + 2):
        game_window.grid_rowconfigure(i, weight=1)

    selected_time_in_seconds = 4 * 60

    start_button = tk.Button(game_window, text="Start Game", command=start_game, font=('Helvetica', 16, 'bold'), bg='green', fg='white', width=20, height=2, state='disabled')
    start_button.grid(row=num_rows + 2, column=1, columnspan=(num_cols//2), pady=10)
    
    random_letter_button = tk.Button(game_window, text="Generate Random Letter", command=generate_random_letter, font=('Helvetica', 16, 'bold'), bg='#e06c75', fg='white', width=20, height=2)
    random_letter_button.grid(row=num_rows + 2, column=(num_cols//2 + 1), columnspan=(num_cols//2), pady=10)

    random_letter_label = tk.Label(game_window, text="Random Letter: ", font=('Helvetica', 16, 'bold'), bg='#1e1e1e', fg='white')
    random_letter_label.grid(row=num_rows + 3, column=1, columnspan=num_cols, pady=10)

    game_window.mainloop()