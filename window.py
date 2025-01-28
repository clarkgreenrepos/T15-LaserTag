import tkinter as tk

def player_screen():
    # Update text to Player Screen
    label.config(text="Player Screen")

# Splash screen
def splash_screen():
    label.pack(pady=20)

# Splash Screen window
root = tk.Tk()
root.title("Team 15") # Window name
root.geometry("1280x720")  # Window size, we can change this whenever but it's easier to work with a smaller window.


# Create a label to display for Splash Screen
label = tk.Label(root, text="Splash Screen", font=("Arial", 16))
splash_screen()

# Continue button
continue_button = tk.Button(root, text="Continue", command=player_screen)
continue_button.pack(pady=10)

# Run
root.mainloop()
