import tkinter as tk

# TODO - set up send and recieve correctly, where the id is sent off and the codename is recieved, I am not entirely sure how to set up 2-way communication with UDP, 
# I could use some help with setting that up -CP

def process_and_move_entry(event):
    entry = event.widget  # Get the specific entry box
    value = entry.get()

    # TODO - create method to send the value to the server and check if the ID sent is valid. If invalid, should return something like -1 to indicate that the value does not match
    # the database. Also add error handling.

    if value:  
        print(f"Value from Entry Box: {value}") 
        entry.delete(0, tk.END)  # Clear the entry box

        # Move the entry box down by 30 pixels
        current_x, current_y = entry.winfo_x(), entry.winfo_y()
        entry.place(x=current_x, y=current_y + 30)

def enter_player(player_id):
    # sends player ID to server, which should go through the database and send back the codename for that ID
    #send(player_id)
    
    return 

def entry_loop(root):
    print("entry loop started")
    
    # TODO - create the graphics for player entry

    # Create 2 entry boxes for red and green
    red_entry = tk.Entry(root)
    green_entry = tk.Entry(root)

    # Place the 2 boxes
    red_entry.place(x=50, y=50)
    green_entry.place(x=200, y=50)

    # Bind enter key to both so when enter is pressed, it submits and moves on
    red_entry.bind("<Return>", process_and_move_entry)
    green_entry.bind("<Return>", process_and_move_entry)


    # Sends off player ID, returns player codename

    