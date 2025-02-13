import tkinter as tk
import asyncio
import threading
from tkinter import PhotoImage
from player import Player
from PIL import Image, ImageTk #requires Pillow install. In terminal, type "pip3 install pillow" or "pip3 install --upgrade pillow" (use "pip" instead of "pip3" for windows.s)
                               #Pillow handles images with alpha. Will be used for images with transparency like many pngs
from udp import * #New class that includes udpSend and udpReceive. See udp.py
    

# Splash screen
def display_splash():
    center_x = (root.winfo_width() - original_image.width) // 2
    center_y = (root.winfo_height() - original_image.height) // 2

    canvas.create_image(center_x, center_y, anchor="nw", image=splash_img)

def remove_splash():
    canvas.delete("all")

def splash_screen(): #will display splash image 3 seconds after startup, remove the image after 8 and show continue button after 12
    root.after(3000, display_splash)
    root.after(6000, remove_splash)
    root.after(12000, player_screen)

#PLAYER SCREEN STUFF

def player_screen(): #player screen main method
    frame = tk.Frame(root, padx = 10, pady = 10) #Creates grid for fields
    frame.place(x = (root.winfo_width() // 2) - 230, y = 100)
    red_label = tk.Label(frame, text = "RED TEAM")
    green_label = tk.Label(frame, text = "GREEN TEAM")
    red_label.grid(row = 0, column = 2)
    green_label.grid(row = 0, column = 5)
    id_label1 = tk.Label(frame, text = "ID No.")
    id_label1.grid(row = 0, column = 1)
    id_label2 = tk.Label(frame, text = "ID No.")
    id_label2.grid(row = 0, column = 4)

    global button_frame
    button_frame = tk.Frame(root, padx = 10, pady = 10) #Creates grid for buttons
    button_frame.place(x = (root.winfo_width() // 2) + 170, y = 100)

    global start_button
    start_button = tk.Button(button_frame, text = "START GAME", command = start_game, bg = "green")
    start_button.grid(row = 2, column = 0)

    global network_button
    network_button = tk.Button(button_frame, text = "Network Address", command = change_network, bg = "blue")
    network_button.grid(row = 0, column = 0)
  

    global reset_button
    reset_button = tk.Button(button_frame, text = "Reset Teams", command = reset_teams, bg = "red")
    reset_button.grid(row = 1, column = 0)


    def create_entry_list(): #create the entry fields and append them to their respective lists. IDs should all be 6 digits. Codenames should be more than 0 but no more than 20 characters.
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
        for i in range(30): #initializes all eqpid indices
            dummyid = "0"
            eqpid_list.append(dummyid)
        for entry in playerid_list:
            entry.bind("<Return>", get_codename) #Enter key will be bound to the ID fields
    create_entry_list()
    
def disable_main(): #disable interactables in main window while a secondary window is active
    for i, entry in enumerate(playerid_list):
        entry.config(state = "readonly")
    start_button['state'] = tk.DISABLED
    network_button['state'] = tk.DISABLED
    reset_button['state'] = tk.DISABLED

def enable_main(): #reenable interactables in main window once secondary window is gone
    for i, entry in enumerate(playerid_list):
        entry.config(state = "normal")
    start_button['state'] = tk.NORMAL
    network_button['state'] = tk.NORMAL
    reset_button['state'] = tk.NORMAL

def reset_teams(): #resets all entries in playerid_list and codename_list. Also, sets the elements in eqpid_list and playerList to "None"
    for i in range(len(playerid_list)):
        playerid_list[i].delete(0, tk.END)
    for i in range(len(codename_list)):
        codename_list[i].config(state = 'normal')
        codename_list[i].delete(0, tk.END)
        codename_list[i].config(state = 'readonly')
    for i in range(len(eqpid_list)):
        eqpid_list[i] = None
    for i in range(len(playerList)):
        playerList[i] = None

def get_codename(event): #check to see if id is valid then check to see if id matches preexisting codename. if no preexisting codename, prompt user for new codename
    entry = event.widget
    id = entry.get() #entered player id
    if len(id) != 6 or not id.isdigit(): # Player IDs must always be 6 digits
        print("invalid id")
    else:
        for i, id_entry in enumerate(playerid_list):#locate which index of the playerid_list the entered id is from
            if id_entry == event.widget:
                print(f"id found at index {i}")
                entry = i
        if check_id(id):
            #TODO create function that querys the database for the corresponding ID. Should return the codename in the form of a string
            print("codename found")
            codename_list[entry].config(state = 'normal')
            codename_list[entry].delete(0, tk.END)
            codename_list[entry].insert(0, "found codename")
            codename_list[entry].config(state = 'readonly')
            get_eqpid(entry)
        else:
            create_codename(entry)

def create_codename(entry_no):
    #create small window for entering new name
    print(f"I'll do index {entry_no} now")

    def submit_codename():
        codename = input_entry.get()
        if 0 < len(codename) <= 20 and character_check(codename):
            codename_list[entry_no].config(state = 'normal')
            codename_list[entry_no].delete(0, tk.END)
            codename_list[entry_no].insert(0, codename)
            codename_list[entry_no].config(state = 'readonly')
            add_codename(entry_no) #This function is further down. It is supposed to give the codename and player ID to the datebase by referencing the "entry_no" (int that represents the index where the codename and id can be found in the playerid_list and codename_list)
            input_window.destroy()
            playerid_list[entry_no].config(state = "normal")
            get_eqpid(entry_no)
        else:
            input_label.config(text = "Invalid Codename", fg = "red")

    def cancel_input():
        input_window.destroy()
        playerid_list[entry_no].config(state = "normal")
        enable_main()

    disable_main()
    input_window = tk.Toplevel(root)
    input_window.title("Input New Codename")
    input_window.geometry("300x200")
    input_window.minsize(300, 200)
    input_window.config(bg = "lightblue")
    input_window.protocol("WM_DELETE_WINDOW", cancel_input)

    playerid_list[entry_no].config(state = "readonly")
    
    input_frame = tk.Frame(input_window, padx = 10, pady = 10)
    input_frame.place(x = 75, y = 50)

    input_label = tk.Label(input_frame, text = "Enter New Codename:")
    input_label.grid(row = 0, column = 0)

    input_entry = tk.Entry(input_frame, width = 20)
    input_entry.grid(row = 1, column = 0)

    input_button = tk.Button(input_frame, text = "Submit", command = submit_codename, bg = "lightgreen")
    input_button.grid(row = 2, column = 0)

    cancel_button = tk.Button(input_frame, text = "Cancel", command = cancel_input, bg = "#E36666")
    cancel_button.grid(row = 3, column = 0)

def check_id(id):
    id = str(id)
    #TODO create function to query the database on whether or not the input ID has a corresponding codename. If no codename, return FALSE
    return False

def add_codename(entry_no):
    #TODO add code to add a new user to the database with their ID and codename
    print("woopy")


#Initialize ip/ports and send/receive sockets to starting values
#TODO add a "current ip" somewhere on the program
udp = Udp("127.0.0.1", 7500, 7501)

import tkinter as tk

def change_network():
    def submit_address():
        network_address = input_entry.get().strip()  # Trim spaces

        # Get the validated IP from validate_ip()
        new_ip = udp.validate_ip(network_address)

        # If input is invalid or unchanged, show an error and keep window open
        if new_ip == udp.get_ip() and network_address != udp.get_ip():
            error_label.config(text="Invalid input.")
            return

        # If valid and different, set new IP and close window
        udp.set_ip(new_ip)
        input_window.destroy()
        enable_main()

    def cancel_input():
        """Closes the input window and re-enables the main window."""
        input_window.destroy()
        enable_main()

   
    disable_main()
    input_window = tk.Toplevel(root)
    input_window.title("Input New Address")
    input_window.geometry("300x200")
    input_window.minsize(300, 200)
    input_window.config(bg="#ffffff")
    input_window.protocol("WM_DELETE_WINDOW", cancel_input)  

    input_frame = tk.Frame(input_window, padx=10, pady=10)
    input_frame.place(relx=0.5, rely=0.4, anchor="center")

    input_label = tk.Label(input_frame, text="Enter New Address:")
    input_label.grid(row=0, column=0, columnspan=2)

    input_entry = tk.Entry(input_frame, width=20)
    input_entry.grid(row=1, column=0, columnspan=2)

 
    button_frame = tk.Frame(input_frame)
    button_frame.grid(row=2, column=0, columnspan=2, pady=5)

    input_button = tk.Button(button_frame, text="Submit", command=submit_address, bg="lightgreen")
    input_button.pack(side="left", padx=5)

    cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_input, bg="#E36666")
    cancel_button.pack(side="left", padx=5)

    error_label = tk.Label(input_frame, text="", fg="red", width=40, anchor="center")
    error_label.grid(row=3, column=0, columnspan=2)




def get_eqpid(entry_no): #prompts user for equipment id then adds it to the corresponding index in the eqpid_list

    def submit_eqpid():
        eqpid = input_entry.get()
        if len(eqpid) == 2 and eqpid.isdigit():
            eqpid_list[entry_no] = eqpid
            print(eqpid_list[entry_no])
            input_window.destroy()
            udp.send_message(f'{eqpid}')
            enable_main()
        else:
            input_label.config(text = "Invalid Equipment ID", fg = "red")

    def cancel_input():
        input_window.destroy()
        playerid_list[entry_no].config(state = "normal")
        playerid_list[entry_no].delete(0, tk.END)
        codename_list[entry_no].delete(0, tk.END)
        enable_main()
        
    input_window = tk.Toplevel(root)
    input_window.title("Input Equipment ID")
    input_window.geometry("300x200")
    input_window.minsize(300, 200)
    input_window.config(bg = "lightblue")
    input_window.protocol("WM_DELETE_WINDOW", cancel_input)
    
    input_frame = tk.Frame(input_window, padx = 10, pady = 10)
    input_frame.place(x = 75, y = 50)

    input_label = tk.Label(input_frame, text = "Enter New Equipment ID:")
    input_label.grid(row = 0, column = 0)

    input_entry = tk.Entry(input_frame, width = 20)
    input_entry.grid(row = 1, column = 0)

    input_button = tk.Button(input_frame, text = "Submit", command = submit_eqpid, bg = "lightgreen")
    input_button.grid(row = 2, column = 0)

    cancel_button = tk.Button(input_frame, text = "Cancel", command = cancel_input, bg = "#E36666")
    cancel_button.grid(row = 3, column = 0)

def character_check(codename):
    special_chars = r"!@#$%^&*()_+\-=\[\]{};\':\"\\|,.<>/?~"
    translation_table = str.maketrans('', '', special_chars)
    return codename.translate(translation_table) == codename


#Start server
def start_udp_receive_task():
    def run_udp():
        asyncio.run(udp.start_receiver())

    
    threading.Thread(target=run_udp, daemon=True).start()

#START GAME STUFF
def start_game():
    # Makes sure there is at least 1 player on both teams
    # this wont work until we make it so players are added to the player list when created
    # redCount = 0
    # greenCount = 0
    # for i in range(15):
    #     if playerList[i]:
    #         redCount += 1
    # for i in range(15, 30):
    #     if playerList[i]:
    #         greenCount += 1
    
    # if greenCount == 0 or redCount == 0:
    #     print("There must be a player on both teams to start")
    #     return    

    start_udp_receive_task() #This works
    udp.send_message("202")

    # Start game loop

    print("Game started")    

# Screen window
root = tk.Tk()
root.title("Photon Super Duper Epic Kool Kid Laser Tag Game for Kool Kidz") # Window name
root.geometry("1280x720+0+0")
root.minsize(700, 500)
root.maxsize(1280, 720)
root.configure(bg="#040333")
original_icon = Image.open("img/T15_icon.png")
icon_img = ImageTk.PhotoImage(original_icon)
root.iconphoto(False, icon_img)

# Create a canvas to display for Splash Screen
canvas = tk.Canvas(root, width=1280, height=720, bg="#040333", bd=0, highlightthickness=0)
canvas.pack()
original_image = Image.open("img/photon_logo.png") # all image files is in the "img" folder
splash_img = ImageTk.PhotoImage(original_image) #photo for the splash screen.
playerid_list = [] #list to hold all of the player ID number entries
codename_list = [] #list to hold all of the player codename entries
eqpid_list = [] #list to hold all of the equipment ID entries
playerList = [None] * 30 #master player list

splash_screen()

# Run
root.mainloop()