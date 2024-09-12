# main_menu.py

import tkinter as tk
from tkinter import messagebox
from game_table import create_editable_grid

def open_main_menu():
    # Create the main menu window
    main_menu = tk.Tk()
    main_menu.title("Anime Game Main Menu")
    
    # Style the main window
    main_menu.configure(bg='#282c34')  # Dark background
    main_menu.geometry("500x400")  # Set window size
    
    # Define the functions for the buttons
    def new_game():
        main_menu.destroy()  # Close the main menu window
        create_editable_grid()  # Open the game window
    
    def check_previous_games():
        messagebox.showinfo("Previous Games", "No previous games found.")
    
    def check_previous_opponents():
        messagebox.showinfo("Previous Opponents", "No previous opponents found.")
    
    def check_stats():
        messagebox.showinfo("Stats", "No stats available.")
    
    # Style for the buttons
    button_style = {
        'font': ('Helvetica', 16, 'bold'),
        'width': 25,
        'height': 2,
        'bg': '#61afef',  # Light blue
        'fg': 'white',    # White text
        'activebackground': '#528bff',  # Darker blue on hover
        'activeforeground': 'white',    # White text on hover
        'relief': 'raised',
        'bd': 5
    }
    
    # Create buttons for the main menu with a nice style
    new_game_button = tk.Button(main_menu, text="New Game", command=new_game, **button_style)
    new_game_button.pack(pady=15)

    prev_games_button = tk.Button(main_menu, text="Check Previous Games", command=check_previous_games, **button_style)
    prev_games_button.pack(pady=15)
    
    prev_opponents_button = tk.Button(main_menu, text="Check Previous Opponents", command=check_previous_opponents, **button_style)
    prev_opponents_button.pack(pady=15)
    
    stats_button = tk.Button(main_menu, text="Check Stats", command=check_stats, **button_style)
    stats_button.pack(pady=15)

    # Create a footer label for extra style
    footer_label = tk.Label(main_menu, text="Anime Game © 2024", bg='#282c34', fg='white', font=('Helvetica', 12, 'italic'))
    footer_label.pack(side='bottom', pady=10)

    # Run the main menu window
    main_menu.mainloop()