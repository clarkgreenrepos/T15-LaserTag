import tkinter as tk
from tkinter import PhotoImage
from playerScreen import PS
from PIL import Image, ImageTk #requires Pillow install. In terminal, type "pip3 install pillow" or "pip3 install --upgrade pillow" (use "pip" instead of "pip3" for windows.s)
                               #Pillow handles images with alpha. Will be used for images with transparency like many pngs

def player_screen(): #player screen main method
    print("woop")
    
# Splash screen
def display_splash():
    center_x = (root.winfo_width() - original_image.width) // 2
    center_y = (root.winfo_height() - original_image.height) // 2

    canvas.create_image(center_x, center_y, anchor="nw", image=splash_img)

def remove_splash():
    canvas.delete("all")

def splash_screen(): #will display splash image 3 seconds after startup, remove the image after 8 and move to player_screen after 12
    root.after(3000, display_splash)
    root.after(8000, remove_splash)
    root.after(12000, player_screen)


# Screen window
root = tk.Tk()
root.title("Photon Super Duper Epic Kool Kid Laser Tag Game for Kool Kidz") # Window name
root.geometry("1280x720")  # Window size, we can change this whenever but it's easier to work with a smaller window.
root.configure(bg="#040333")


# Create a canvas to display for Splash Screen
canvas = tk.Canvas(root, width=1280, height=720, bg="#040333", bd=0, highlightthickness=0)
canvas.pack()
original_image = Image.open("img/photon_logo.png") # all image files is in the "img" folder
splash_img = ImageTk.PhotoImage(original_image) #photo for the splash screen. this will change to the photon logo eventually
splash_screen()


# Continue button
#continue_button = tk.Button(root, text="Continue", command=player_screen)
#continue_button.pack(pady=10)

# Run
root.mainloop()