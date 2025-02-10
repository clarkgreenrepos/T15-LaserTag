import tkinter as tk
from tkinter import PhotoImage
from playerEntry import entry_loop
from player import Player
from PIL import Image, ImageTk #requires Pillow install. In terminal, type "pip3 install pillow" or "pip3 install --upgrade pillow" (use "pip" instead of "pip3" for windows.s)
                               #Pillow handles images with alpha. Will be used for images with transparency like many pngs
    
# Splash screen
def display_splash():
    center_x = (root.winfo_width() - original_image.width) // 2
    center_y = (root.winfo_height() - original_image.height) // 2

    canvas.create_image(center_x, center_y, anchor="nw", image=splash_img)

def remove_splash():
    canvas.delete("all")

def splash_screen(): #will display splash image 3 seconds after startup, remove the image after 8 and show continue button after 12
    root.after(3000, display_splash)
    root.after(8000, remove_splash)
    root.after(12000, player_screen)

#Player Screen Stuff

def player_screen(): #player screen main method
    frame = tk.Frame(root, padx = 10, pady = 10) #Creates grid for fields and buttons
    frame.place(x = (root.winfo_width() // 2) - 230, y = 100)
    red_label = tk.Label(frame, text = "RED TEAM")
    green_label = tk.Label(frame, text = "GREEN TEAM")
    red_label.grid(row = 0, column = 2)
    green_label.grid(row = 0, column = 5)
    id_label1 = tk.Label(frame, text = "ID No.")
    id_label1.grid(row = 0, column = 1)
    id_label2 = tk.Label(frame, text = "ID No.")
    id_label2.grid(row = 0, column = 4)
    playerid_list = [] #list to hold all of the player ID numbers
    codename_list = [] #list to hold all of the player codenames
   
    def create_entry_list(): #create the entry fields and append them to their respective lists
        for i in range(15): #RED TEAM entry fields. index 0 - 14 in the codename and player ID lists
            entryNo = tk.Label(frame, width = 2, text = f"{i + 1}")
            entryNo.grid(row = i + 1, column = 0)

            playerid = tk.Entry(frame, width = 6)
            playerid.grid(row = i + 1, column = 1)
            playerid_list.append(playerid)

            codename = tk.Entry(frame, width = 20, state = 'readonly')
            codename.grid(row = i + 1, column = 2)
            codename_list.append(codename)
        for i in range(15): #GREEN TEAM entry fields. index 15 - 29 in the codename and player ID lists
            entryNo = tk.Label(frame, width = 2, text = f"{i + 1}")
            entryNo.grid(row = i + 1, column = 3)
            
            playerid = tk.Entry(frame, width = 6)
            playerid.grid(row = i + 1, column = 4)
            playerid_list.append(playerid)

            codename = tk.Entry(frame, width = 20, state = 'readonly')
            codename.grid(row = i + 1, column = 5)
            codename_list.append(codename)
        for entry in playerid_list:
            entry.bind("<Return>", submit_player) #Enter key will be bound to the ID fields
    create_entry_list()
    
    print("woop")

def submit_player(event):
    print("check for valid ID")
    entry = event.widget
    id = entry.get()
    if len(id) <= 6:
        print("valid id")
    else:
        print("invalid id")
    
def show_continue_button():
    continue_button.place(relx=0.5, rely=0.5, anchor="center")
    root.update()

def remove_continue_button():
    continue_button.place_forget()

# Screen window
root = tk.Tk()
root.title("Photon Super Duper Epic Kool Kid Laser Tag Game for Kool Kidz") # Window name
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")  # Window size, will automatically adjust to the host machine's screen size
root.minsize(700, 500)
root.configure(bg="#040333")



# Create a canvas to display for Splash Screen
canvas = tk.Canvas(root, width=1280, height=720, bg="#040333", bd=0, highlightthickness=0)
canvas.pack()
original_image = Image.open("img/photon_logo.png") # all image files is in the "img" folder
splash_img = ImageTk.PhotoImage(original_image) #photo for the splash screen.
playerList = [30]

splash_screen()


# Continue button
# TODO - make continue button less ugly
continue_button = tk.Button(root, text="Continue", command=player_screen, bg="lightgray")

# Run
root.mainloop()