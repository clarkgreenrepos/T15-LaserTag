import tkinter as tk
import asyncio
import threading
from tkinter import PhotoImage
from player import Player
from PIL import Image, ImageTk #requires Pillow install. In terminal, type "pip3 install pillow" or "pip3 install --upgrade pillow" (use "pip" instead of "pip3" for windows.s)
                               #Pillow handles images with alpha. Will be used for images with transparency like many pngs
from udp import * #New class that includes udpSend and udpReceive. See udp.py
    

# Splash screen
def displaySplash():
    centerX = (root.winfo_width() - originalImage.width) // 2
    centerY = (root.winfo_height() - originalImage.height) // 2

    canvas.create_image(centerX, centerY, anchor="nw", image=splashImage)

#PLAYER SCREEN STUFF
def playerScreen(): #player screen main method
    frame = tk.Frame(root, padx = 10, pady = 10) #Creates grid for fields
    frame.place(x = (root.winfo_width() // 2) - 230, y = 100)
    redLabel = tk.Label(frame, text = "RED TEAM")
    greenLabel = tk.Label(frame, text = "GREEN TEAM")
    redLabel.grid(row = 0, column = 2)
    greenLabel.grid(row = 0, column = 5)
    idLabel1 = tk.Label(frame, text = "P ID No.")
    idLabel1.grid(row = 0, column = 1)
    idLabel2 = tk.Label(frame, text = "P ID No.")
    idLabel2.grid(row = 0, column = 4)

    global buttonFrame
    buttonFrame = tk.Frame(root, padx = 10, pady = 10) #Creates grid for buttons
    buttonFrame.place(x = (root.winfo_width() // 2) + 170, y = 100)

    global startButton
    startButton = tk.Button(buttonFrame, text = "START GAME", command = startGame, bg = "green")
    startButton.grid(row = 2, column = 0)

    global networkButton
    networkButton = tk.Button(buttonFrame, text = "Network Address", command = changeNetwork, bg = "blue")
    networkButton.grid(row = 0, column = 0)
  

    global resetButton
    resetButton = tk.Button(buttonFrame, text = "Reset Teams", command = resetTeams, bg = "red")
    resetButton.grid(row = 1, column = 0)


    def createEntryList(): #create the entry fields and append them to their respective lists. IDs should all be 6 digits. Codenames should be more than 0 but no more than 20 characters.
        for i in range(15): #RED TEAM entry fields. index 0 - 14 in the codename and player ID lists
            entryNo = tk.Label(frame, width = 2, text = f"{i + 1}")
            entryNo.grid(row = i + 1, column = 0)

            playerId = tk.Entry(frame, width = 6)
            playerId.grid(row = i + 1, column = 1)
            playerIdList.append(playerId)

            codename = tk.Entry(frame, width = 20, state = 'readonly')
            codename.grid(row = i + 1, column = 2)
            codenameList.append(codename)
        for i in range(15): #GREEN TEAM entry fields. index 15 - 29 in the codename and player ID lists
            entryNo = tk.Label(frame, width = 2, text = f"{i + 1}")
            entryNo.grid(row = i + 1, column = 3)
            
            playerId = tk.Entry(frame, width = 6)
            playerId.grid(row = i + 1, column = 4)
            playerIdList.append(playerId)

            codename = tk.Entry(frame, width = 20, state = 'readonly')
            codename.grid(row = i + 1, column = 5)
            codenameList.append(codename)
        for i in range(30): #initializes all eqpid indices
            dummyId = "0"
            equipmentIdList.append(dummyId)
        for entry in playerIdList:
            entry.bind("<Return>", getCodename) #Enter key will be bound to the ID fields
    createEntryList()
   
    
def toggleMain(on: bool):
    newConfigState = "normal" if on == True else "readonly"
    newButtonState = tk.NORMAL if on == True else tk.DISABLED
    for i, entry in enumerate(playerIdList):
        entry.config(state = newConfigState)
    startButton['state'] = newButtonState
    networkButton['state'] = newButtonState
    resetButton['state'] = newButtonState
    

def resetTeams(): #resets all entries in playerIdList and codenameList. Also, sets the elements in equipmentIdList and playerList to "None"
    for i in range(len(playerIdList)):
        playerIdList[i].delete(0, tk.END)
    for i in range(len(codenameList)):
        codenameList[i].config(state = 'normal')
        codenameList[i].delete(0, tk.END)
        codenameList[i].config(state = 'readonly')
    for i in range(len(equipmentIdList)):
        equipmentIdList[i] = None
    for i in range(len(playerList)):
        playerList[i] = None


def getCodename(event): #check to see if id is valid then check to see if id matches preexisting codename. if no preexisting codename, prompt user for new codename
    entry = event.widget
    id = entry.get() #entered player id
    if len(id) != 6 or not id.isdigit(): # Player IDs must always be 6 digits
        print("invalid id")
    else:
        for i, idEntry in enumerate(playerIdList):#locate which index of the playerIdList the entered id is from
            if idEntry == event.widget:
                print(f"id found at index {i}")
                entry = i
        if checkId(id):
            #TODO create function that querys the database for the corresponding ID. Should return the codename in the form of a string
            print("codename found")
            codenameList[entry].config(state = 'normal')
            codenameList[entry].delete(0, tk.END)
            codenameList[entry].insert(0, "found codename")
            codenameList[entry].config(state = 'readonly')
            getEquipmentId(entry)
        else:
            createCodename(entry)


def createCodename(entryNumber):
    #create small window for entering new name
    print(f"I'll do index {entryNumber} now")

    def submitCodename():
        codename = inputEntry.get()
        if 0 < len(codename) <= 20 and characterCheck(codename):
            codenameList[entryNumber].config(state = 'normal')
            codenameList[entryNumber].delete(0, tk.END)
            codenameList[entryNumber].insert(0, codename)
            codenameList[entryNumber].config(state = 'readonly')
            addCodename(entryNumber) #This function is further down. It is supposed to give the codename and player ID to the datebase by referencing the "entryNumber" (int that represents the index where the codename and id can be found in the playerIdList and codenameList)
            inputWindow.destroy()
            getEquipmentId(entryNumber)
        else:
            inputLabel.config(text = "Invalid Codename", fg = "red")

    def cancelInput():
        inputWindow.destroy()
        playerIdList[entryNumber].config(state = "normal")
        toggleMain(True)

    toggleMain(False)
    inputWindow = tk.Toplevel(root)
    inputWindow.title("Input New Codename")
    inputWindow.geometry("300x200")
    inputWindow.minsize(300, 200)
    inputWindow.config(bg = "lightblue")
    inputWindow.protocol("WM_DELETE_WINDOW", cancelInput)

    playerIdList[entryNumber].config(state = "readonly")
    
    inputFrame = tk.Frame(inputWindow, padx = 10, pady = 10)
    inputFrame.place(x = 75, y = 50)

    inputLabel = tk.Label(inputFrame, text = "Enter New Codename:")
    inputLabel.grid(row = 0, column = 0)

    inputEntry = tk.Entry(inputFrame, width = 20)
    inputEntry.grid(row = 1, column = 0)

    inputButton = tk.Button(inputFrame, text = "Submit", command = submitCodename, bg = "lightgreen")
    inputButton.grid(row = 2, column = 0)

    cancelButton = tk.Button(inputFrame, text = "Cancel", command = cancelInput, bg = "#E36666")
    cancelButton.grid(row = 3, column = 0)


def checkId(id):
    id = str(id)
    #TODO create function to query the database on whether or not the input ID has a corresponding codename. If no codename, return FALSE
    return False


def addCodename(entryNumber):
    #TODO add code to add a new user to the database with their ID and codename
    print("woopy")


def changeNetwork():
    def submitAddress():
        networkAddress = inputEntry.get().strip()  # Trim spaces

        # If input is invalid or unchanged, show an error and keep window open

        if not udp.setIp(networkAddress):
            errorLabel.config(text="Invalid input.")
            return

        inputWindow.destroy()
        toggleMain(True)

    def cancelInput():
        """Closes the input window and re-enables the main window."""
        inputWindow.destroy()
        toggleMain(True)

   
    toggleMain(False)
    inputWindow = tk.Toplevel(root)
    inputWindow.title("Input New Address")
    inputWindow.geometry("300x200")
    inputWindow.minsize(300, 200)
    inputWindow.config(bg="#ffffff")
    inputWindow.protocol("WM_DELETE_WINDOW", cancelInput)  

    inputFrame = tk.Frame(inputWindow, padx=10, pady=10)
    inputFrame.place(relx=0.5, rely=0.4, anchor="center")

    inputLabel = tk.Label(inputFrame, text="Enter New Address:")
    inputLabel.grid(row=0, column=0, columnspan=2)

    inputEntry = tk.Entry(inputFrame, width=20)
    inputEntry.grid(row=1, column=0, columnspan=2)

 
    buttonFrame = tk.Frame(inputFrame)
    buttonFrame.grid(row=2, column=0, columnspan=2, pady=5)

    inputButton = tk.Button(buttonFrame, text="Submit", command=submitAddress, bg="lightgreen")
    inputButton.pack(side="left", padx=5)

    cancelButton = tk.Button(buttonFrame, text="Cancel", command=cancelInput, bg="#E36666")
    cancelButton.pack(side="left", padx=5)

    errorLabel = tk.Label(inputFrame, text="", fg="red", width=40, anchor="center")
    errorLabel.grid(row=3, column=0, columnspan=2)


def getEquipmentId(entryNumber): #prompts user for equipment id then adds it to the corresponding index in the equipmentIdList

    def submitEquipmentId():
        equipmentId = inputEntry.get()
        if len(equipmentId) == 2 and equipmentId.isdigit():
            equipmentIdList[entryNumber] = equipmentId
            print(equipmentIdList[entryNumber])
            inputWindow.destroy()
            udp.sendMessage(f'{equipmentId}')
            toggleMain(True)
        else:
            inputLabel.config(text = "Invalid Equipment ID", fg = "red")

    def cancelInput():
        inputWindow.destroy()
        playerIdList[entryNumber].config(state = "normal")
        playerIdList[entryNumber].delete(0, tk.END)
        codenameList[entryNumber].delete(0, tk.END)
        toggleMain(True)
        
    inputWindow = tk.Toplevel(root)
    inputWindow.title("Input Equipment ID")
    inputWindow.geometry("300x200")
    inputWindow.minsize(300, 200)
    inputWindow.config(bg = "lightblue")
    inputWindow.protocol("WM_DELETE_WINDOW", cancelInput)
    
    inputFrame = tk.Frame(inputWindow, padx = 10, pady = 10)
    inputFrame.place(x = 75, y = 50)

    inputLabel = tk.Label(inputFrame, text = "Enter New Equipment ID:")
    inputLabel.grid(row = 0, column = 0)

    inputEntry = tk.Entry(inputFrame, width = 20)
    inputEntry.grid(row = 1, column = 0)

    inputButton = tk.Button(inputFrame, text = "Submit", command = submitEquipmentId, bg = "lightgreen")
    inputButton.grid(row = 2, column = 0)

    cancelButton = tk.Button(inputFrame, text = "Cancel", command = cancelInput, bg = "#E36666")
    cancelButton.grid(row = 3, column = 0)


def characterCheck(codename):
    specialChars = r"!@#$%^&*()_+\-=\[\]{};\':\"\\|,.<>/?~"
    translationTable = str.maketrans('', '', specialChars)
    return codename.translate(translationTable) == codename

#Start server
def startUdpReceiveTask():
    def runUdp():
        asyncio.run(udp.startReceiver())

    
    threading.Thread(target=runUdp, daemon=True).start()

#START GAME STUFF
def startGame():
    # Makes sure there is at least 1 player on both teams
    # this wont work until we make it so players are added to the player list when created
    redCount = 0
    greenCount = 0
    # for i in range(15):
    #     if playerList[i]:
    #         redCount += 1
    # for i in range(15, 30):
    #     if playerList[i]:
    #         greenCount += 1

    def makePlayerList(): # Add the contents of the 3 entry lists to the Player List
        nonlocal redCount, greenCount
        for i in range(30):
            playerId = playerIdList[i].get()
            codename = codenameList[i].get()
            equipmentId = equipmentIdList[i]

            # if the index of the current player is 0 - 14, red team. 15 - 29 is green team
            if playerId != "" and i <= 14: 
                playerList[i] = Player(playerId, codename, equipmentId, 0)
                redCount += 1
            elif playerId != "" and 14 < i <= 29:
                playerList[i] = Player(playerId, codename, equipmentId, 1)
                greenCount += 1
    
    makePlayerList()

    if greenCount == 0 or redCount == 0:
        print("There must be a player on both teams to start")
        return    

    for i in range(30):
        if playerList[i] != None:
            print(f"{i}: {playerList[i].ID}, {playerList[i].Codename}, {playerList[i].EqpID}, {playerList[i].Team}")

    startUdpReceiveTask() #This works
    udp.sendMessage("202")

    # Start game loop

    print("Game started")    

#Initialize ip/ports and send/receive sockets to starting values
#TODO add a "current ip" somewhere on the program
udp = Udp("127.0.0.1", 7500, 7501)

# Screen window
root = tk.Tk()
root.title("Photon Super Duper Epic Kool Kid Laser Tag Game for Kool Kidz") # Window name
root.geometry("1280x720+0+0")
root.minsize(700, 500)
root.maxsize(1280, 720)
root.configure(bg="#040333")
originalIcon = Image.open("img/T15_icon.png")
iconImage = ImageTk.PhotoImage(originalIcon)
root.iconphoto(False, iconImage)

# Create a canvas to display for Splash Screen
canvas = tk.Canvas(root, width=1280, height=720, bg="#040333", bd=0, highlightthickness=0)
canvas.pack()
originalImage = Image.open("img/photon_logo.png") # all image files is in the "img" folder
splashImage = ImageTk.PhotoImage(originalImage) #photo for the splash screen.
playerIdList = [] #list to hold all of the player ID number entries
codenameList = [] #list to hold all of the player codename entries
equipmentIdList = [] #list to hold all of the equipment ID entries
playerList = [None] * 30 #master player list

#will display splash image after startup then remove the image the show player screen
root.after(3000, displaySplash)
root.after(6000, lambda: canvas.delete("all"))
root.after(7000, playerScreen)

# Run
root.mainloop()