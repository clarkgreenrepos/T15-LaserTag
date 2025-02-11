import tkinter as tk
import asyncio
import socket
import threading
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

#PLAYER SCREEN STUFF

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

    start_button = tk.Button(root, text = "START GAME", command = start_game, bg = "green")
    start_button.place(x = (root.winfo_width() // 2) + 50, y = root.winfo_height() // 2)

    network_button = tk.Button(root, text = "Network Address", command = change_network, bg = "blue")
    network_button.place(x = (root.winfo_width() // 2) -100, y = root.winfo_height() // 2)

    start_udp_receive_task()

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
        for entry in playerid_list:
            entry.bind("<Return>", get_codename) #Enter key will be bound to the ID fields
    create_entry_list()
    
    print("woop")

def get_codename(event): #check to see if id is valid then check to see if id matches preexisting codename. if no preexisting codename, prompt user for new codename
    entry = event.widget
    id = entry.get() #entered player id
    if len(id) != 6: # Player IDs must always be 6 digits
        print("invalid id")
    else:
        for i, id_entry in enumerate(playerid_list):#locat which index of the playerid_list the entered id is from
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
            
        else:
            create_codename(entry)

def create_codename(entry_no):
    #create small window for entering new name
    print(f"I'll do index {entry_no} now")

    def submit_codename():
        codename = input_entry.get()
        if 0 < len(codename) <= 20:
            codename_list[entry_no].config(state = 'normal')
            codename_list[entry_no].delete(0, tk.END)
            codename_list[entry_no].insert(0, codename)
            codename_list[entry_no].config(state = 'readonly')
            add_codename(entry_no) #This function is further down. It is supposed to give the codename and player ID to the datebase by referencing the "entry_no" (int that represents the index where the codename and id can be found in the playerid_list and codename_list)
            input_window.destroy()
            root.attributes("-disable", False)
        else:
            input_label.config(text = "Invalid Codename", fg = "red")

    def cancel_input():
        input_window.destroy()
        root.attributes("-disable", False) #reenables the main window

    root.attributes("-disable", True) #disables main window while input window is active
    input_window = tk.Toplevel(root)
    input_window.title("Input New Codename")
    input_window.geometry("300x200")
    input_window.minsize(300, 200)
    input_window.config(bg = "lightblue")
    
    input_frame = tk.Frame(input_window, padx = 10, pady = 10)
    input_frame.place(x = 75, y = 50)

    input_label = tk.Label(input_frame, text = "Enter New Codename:")
    input_label.grid(row = 0, column = 0)

    input_entry = tk.Entry(input_frame, width = 20)
    input_entry.grid(row = 1, column = 0)

    input_button = tk.Button(input_frame, text = "Submit", command = submit_codename, bg = "lightgreen")
    input_button.grid(row = 2, column = 0)

    cancel_button = tk.Button(input_frame, text = "Cancel", command = cancel_input, bg = "lightred")
    cancel_button.grid(row = 3, column = 0)

def check_id(id):
    id = str(id)
    #TODO create function to query the database on whether or not the input ID has a corresponding codename. If no codename, return FALSE
    return False

def add_codename(entry_no):
    #TODO add code to add a new user to the database with their ID and codename
    print("woopy")

def change_network():
    #TODO add a function for changing the active network address
    print("i don't wanna")

# UDP SERVER STUFF
def start_udp_receive_task():
    # Runs UDP client on a seperate thread so tkinter is not blocked
    def run_udp():
        asyncio.run(udp_client_receive())

    threading.Thread(target=run_udp, daemon=True).start()

class UDPHandler(asyncio.DatagramProtocol):
    def datagram_received(self, data, addr):
        message = data.decode().strip()
        print(f"Received from {addr}: {message}")
        # TODO - update GUI with received codename or handle new codename entry

async def udp_client_receive(ip="127.0.0.1", port=7501):
    loop = asyncio.get_running_loop()

    print(f"Starting UDP client receive on {ip}:{port}")
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UDPHandler(),
        local_addr=(ip, port)
    )

    print(f"Listening for UDP receives on {ip}:{port}")

    try:
        await asyncio.Event().wait()  # Run indefinitely
    finally:
        transport.close()

#START GAME STUFF
def start_game():

    #TODO create start game function that moves to the game action screen
    print("no")
    

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
playerid_list = [] #list to hold all of the player ID number entries
codename_list = [] #list to hold all of the player codename entries
playerList = [30] #master player list

splash_screen()

# Run
root.mainloop()