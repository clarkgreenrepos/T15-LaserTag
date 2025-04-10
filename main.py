import tkinter as tk
import asyncio
import threading
import psycopg2
import os
import time
import sys
import random
import pygame

from tkinter import PhotoImage
from tkinter import messagebox
from player import Player
from PIL import (
    Image,
    ImageTk,
)  # requires Pillow install. In terminal, type "pip3 install pillow" or "pip3 install --upgrade pillow" (use "pip" instead of "pip3" for windows.s)

# Pillow handles images with alpha. Will be used for images with transparency like many pngs
from udp import *  # New class that includes udpSend and udpReceive. See udp.py


# Splash screen
def displaySplash():
    centerX = (root.winfo_width() - originalImage.width) // 2
    centerY = (root.winfo_height() - originalImage.height) // 2

    canvas.create_image(centerX, centerY, anchor="nw", image=splashImage)

# PLAYER SCREEN STUFF
def playerScreen():  # player screen main method
    frame = tk.Frame(root, name="playerScreen")  # Creates grid for fields
    frame.place(in_=root, anchor="c", relx=.5, rely=.5)
    
    #frame for all of the inputs
    inputs = tk.Frame(frame, bg="yellow") #if you see yellow this is unintentional
    inputs.grid(row=0, column=0)

    #The input frame is divided into two smaller fames for each team
    redFrame = tk.Frame(inputs, padx=10, pady=10, bg="red")
    redFrame.grid(row=0, column=0)
    greenFrame = tk.Frame(inputs, padx=10, pady=10, bg="green")
    greenFrame.grid(row=0, column=1)
    
    #red Team Labels 
    redLabel = tk.Label(redFrame, text="RED TEAM", bg="red")
    redLabel.grid(row=0, column=2)
    idLabel1 = tk.Label(redFrame, text="P ID No.", bg="red")
    idLabel1.grid(row=0, column=1)
    
    #Green Team Labels
    greenLabel = tk.Label(greenFrame, text="GREEN TEAM", bg="green")
    greenLabel.grid(row=0, column=2)
    idLabel2 = tk.Label(greenFrame, text="P ID No.", bg="green")
    idLabel2.grid(row=0, column=1)
    
    #frame For Controls
    controls = tk.Frame(frame, pady=20)
    controls.grid(row=1, column=0)

    root.bind("<F5>", lambda event: resetTeams())  # Bind keys
    root.bind("<F12>", lambda event: preGameErrorCheck())

    global startButton
    startButton = tk.Button(controls, text="START GAME", command=preGameErrorCheck, bg="green")
    startButton.grid(row=0, column=2)

    global networkButton
    networkButton = tk.Button(controls, text="Network Address", command=changeNetwork, bg="blue")
    networkButton.grid(row=0, column=0)

    global resetButton
    resetButton = tk.Button(controls, text="Reset Teams", command=resetTeams, bg="red")
    resetButton.grid(row=0, column=4)

    # create the entry fields and append them to their respective lists. IDs should all be 6 digits. Codenames should be more than 0 but no more than 20 characters.
    for j in range(2):
        color = ["red", "green"]
        currentFrame = [redFrame,greenFrame]
        # RED TEAM entry fields. index 0 - 14 in the codename and player ID lists 
        # GREEN TEAM entry fields. index 15 - 29 in the codename and player ID lists
        for i in range(15):  
            entryNo = tk.Label(currentFrame[j], width=2, text=f"{i + 1}",bg=color[j])
            entryNo.grid(row=i + 1, column=0)

            playerId = tk.Entry(currentFrame[j], width=6, highlightbackground=color[j])
            playerId.grid(row=i + 1, column=1)
            playerIdList.append(playerId)

            codename = tk.Entry(currentFrame[j], width=20, state="readonly", highlightbackground=color[j], readonlybackground="#E0E0E0", justify="center")
            codename.grid(row=i + 1, column=2)
            if(i == 0):
                codename.config(state="normal")
                codename.insert(0, "<--- Enter ID & Press Enter")
                codename.config(state="readonly")
            
            codenameList.append(codename)
            
    for i in range(30):  # initializes all eqpid indices
        dummyId = "0"
        equipmentIdList.append(dummyId)
            
    for entry in playerIdList:
        entry.bind("<Return>", getCodename)  # Enter key will be bound to the ID fields


#game Screen
def gameScreen():
    global redGameLabels, greenGameLabels, actionList, gameTime
    
    mainFrame = tk.Frame(root, padx=10, pady=10, bg="black",highlightbackground="white", highlightthickness=5)
    mainFrame.place(in_=root, anchor="c", relx=.5, rely=.5)
    root.title("Team Layout")

    # Create frames for each column
    redFrame = tk.Frame(mainFrame, bg="red")
    redFrame.grid(row=0, column=0, rowspan=15, padx=2, pady=2)

    middleFrame = tk.Frame(mainFrame, bg="black")
    middleFrame.grid(row=0, column=1, rowspan=15, padx=2, pady=2)

    greenFrame = tk.Frame(mainFrame, bg="green")
    greenFrame.grid(row=0, column=2, rowspan=15, padx=2, pady=2)

    # Labels for RED and GREEN columns
    tk.Label(redFrame, text="RED", font=("Arial", 14, "bold"), pady=5, bg="red", fg="white").grid(row=0, column=0)
    tk.Label(greenFrame, text="GREEN", font=("Arial", 14, "bold"), pady=5, bg="green", fg="white").grid(row=0, column=0)

    # Create placeholders under RED, MIDDLE, and GREEN columns
    for i in range(1, 16):
        # Red team labels
        redLabel = tk.Label(redFrame, text="", width=30, relief="flat", bg="red", fg="white")
        redLabel.grid(row=i, column=0, padx=2, pady=2)
        redGameLabels.append(redLabel)

        # Green team labels
        greenLabel = tk.Label(greenFrame, text="", width=30, relief="flat", bg="green", fg="white")
        greenLabel.grid(row=i, column=0, padx=2, pady=2)
        greenGameLabels.append(greenLabel)

        # Action column labels
        actionLabel = tk.Label(middleFrame, text="", width=30, relief="flat", bg="black", fg="white")
        actionLabel.grid(row=i, column=0, padx=2, pady=2)
        actionList.append(actionLabel)

    udp.sendMessage("202")

    # Start a 6 min countdown
    gameTime = 360

    # Populate labels with player IDs
    root.after(1000, updatePlayers)

    root.mainloop()

def gameMusic():
    number = random.randint(1, 8)
    pygame.mixer.init()
    if number == 1:
        pygame.mixer.music.load('sound/Track01.mp3')
    elif number == 2:
        pygame.mixer.music.load('sound/Track02.mp3')
    elif number == 3:
        pygame.mixer.music.load('sound/Track03.mp3')
    elif number == 4:
        pygame.mixer.music.load('sound/Track04.mp3')
    elif number == 5:
        pygame.mixer.music.load('sound/Track05.mp3')
    elif number == 6:
        pygame.mixer.music.load('sound/Track06.mp3')
    elif number == 7:
        pygame.mixer.music.load('sound/Track07.mp3')
    elif number == 8:
        pygame.mixer.music.load('sound/Track08.mp3')
    
    pygame.mixer.music.play()

    gameScreen()

def updatePlayers():
    # TODO: Create function that sorts playerlist for red and green by score and call it here
    global gameTime
    print(f"{gameTime} seconds remaining")
    gameTime -= 1

    for i in range(15):
        if i < len(playerList) and playerList[i] is not None:
            redGameLabels[i].config(text=f"{playerList[i].Codename} - {playerList[i].Score}")

    for i in range(15, 30):
        if i < len(playerList) and playerList[i] is not None:
            greenGameLabels[i - 15].config(text=f"{playerList[i].Codename} - {playerList[i].Score}")

    root.after(1000, updatePlayers)


def toggleMain(on: bool):
    newConfigState = "normal" if on == True else "readonly"
    newButtonState = tk.NORMAL if on == True else tk.DISABLED
    for i, entry in enumerate(playerIdList):
        entry.config(state=newConfigState)
    startButton["state"] = newButtonState
    networkButton["state"] = newButtonState
    resetButton["state"] = newButtonState
    root.bind("<F5>", lambda event: resetTeams()) if on == True else root.unbind("<F5>")
    (
        root.bind("<F12>", lambda event: preGameErrorCheck())
        if on == True
        else root.unbind("<F12>")
    )


def resetTeams():  # resets all entries in playerIdList and codenameList. Also, sets the elements in equipmentIdList and playerList to "None"
    for i in range(len(playerIdList)):
        playerIdList[i].delete(0, tk.END)
    for i in range(len(codenameList)):
        codenameList[i].config(state="normal")
        codenameList[i].delete(0, tk.END)
        codenameList[i].config(state="readonly")
    for i in range(len(equipmentIdList)):
        equipmentIdList[i] = None
    for i in range(len(playerList)):
        playerList[i] = None


def getCodename(
    event,
):  # check to see if id is valid then check to see if id matches preexisting codename. if no preexisting codename, prompt user for new codename
    entry = event.widget
    id = entry.get()  # entered player id

    if len(id) != 6 or not id.isdigit():  # Player IDs must always be 6 digits
        print("invalid id")
        messagebox.showwarning(title="Invalid ID", message="Id must be a 6 digits long number")
        return

    # Find the entry index
    entry_index = None
    for i, id_entry in enumerate(
        playerIdList
    ):  # locate which index of the playerid_list the entered id is from
        if id_entry == entry:
            print(f"id found at index {i}")
            entry_index = i
            break

    if entry_index is None:
        print("Error: Could not determine index")
        return

    if checkId(id):
        print("codename found")
        codename = getCodenameFromDB(id)
        codenameList[entry_index].config(state="normal")
        codenameList[entry_index].delete(0, tk.END)
        codenameList[entry_index].insert(0, codename)
        codenameList[entry_index].config(state="readonly")
        getEquipmentId(entry_index)
    else:
        for i, idEntry in enumerate(
            playerIdList
        ):  # locate which index of the playerIdList the entered id is from
            if idEntry == event.widget:
                print(f"id found at index {i}")
                entry = i
        if checkId(id):
            print("codename found")
            codename = getCodenameFromDB(id)
            codenameList[entry_index].config(state="normal")
            codenameList[entry_index].delete(0, tk.END)
            codenameList[entry_index].insert(0, codename)
            codenameList[entry_index].config(state="readonly")
            getEquipmentId(entry_index)
        else:
            createCodename(entry_index)


def createCodename(entryNumber):
    # create small window for entering new name
    print(f"Creating codename at ID {entryNumber}")

    def submitCodename():
        codename = inputEntry.get()
        if 0 < len(codename) <= 20 and characterCheck(codename):
            codenameList[entryNumber].config(state="normal")
            codenameList[entryNumber].delete(0, tk.END)
            codenameList[entryNumber].insert(0, codename)
            codenameList[entryNumber].config(state="readonly")
            addCodename(
                entryNumber
            )  # This function is further down. It is supposed to give the codename and player ID to the datebase by referencing the "entryNumber" (int that represents the index where the codename and id can be found in the playerIdList and codenameList)
            inputWindow.destroy()
            getEquipmentId(entryNumber)
        else:
            inputLabel.config(text="Invalid Codename", fg="red")

    def cancelInput():
        inputWindow.destroy()
        playerIdList[entryNumber].config(state="normal")
        toggleMain(True)

    toggleMain(False)
    inputWindow = tk.Toplevel(root)
    inputWindow.title("Input New Codename")
    inputWindow.geometry("300x200")
    inputWindow.minsize(300, 200)
    inputWindow.config(bg="lightblue")
    inputWindow.protocol("WM_DELETE_WINDOW", cancelInput)

    playerIdList[entryNumber].config(state="readonly")

    inputFrame = tk.Frame(inputWindow, padx=10, pady=10)
    inputFrame.place(x=75, y=50)

    inputLabel = tk.Label(inputFrame, text="Enter New Codename:")
    inputLabel.grid(row=0, column=0)

    inputEntry = tk.Entry(inputFrame, width=20)
    inputEntry.grid(row=1, column=0)

    inputButton = tk.Button(
        inputFrame, text="Submit", command=submitCodename, bg="lightgreen"
    )
    inputButton.grid(row=2, column=0)

    cancelButton = tk.Button(
        inputFrame, text="Cancel", command=cancelInput, bg="#E36666"
    )
    cancelButton.grid(row=3, column=0)

# Establish database connection
def connect_db():
    # bypass database if "test" passed in on compile
    if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        return
    
    try:
        conn = psycopg2.connect(
            dbname="photon",
            user="student",
            password="student",
            host="localhost",
            port="5432",
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to database")
        return None


def checkId(id):
    # bypass database if "test" passed in on compile
    if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        return False
    
    id = str(id)

    conn = connect_db()
    if conn is None:
        return False

    cur = conn.cursor()
    cur.execute("select codename from players where id = %s;", (id,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    if result is not None:
        print(f"ID {id} found in database with codename: {result[0]}")
        return True
    else:
        print(f"ID {id} not found in the database.")
        return False


def addCodename(entryNumber):
    # TODO add code to add a new user to the database with their ID and codename
    player_id = playerIdList[entryNumber].get()
    codename = codenameList[entryNumber].get()

    conn = connect_db()
    if conn is None:
        return

    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO players (id, codename) SELECT %s, %s WHERE NOT EXISTS (SELECT 1 FROM players WHERE id = %s)",
            (player_id, codename, player_id),
        )
        conn.commit()
    except psycopg2.Error as e:
        print("Error inserting data", e)
    finally:
        cur.close()
        conn.close()


def getCodenameFromDB(player_id):
    """Fetch the codename for a given player ID from the database."""
    conn = connect_db()
    if conn is None:
        print("Database connection failed")
        return None

    cur = conn.cursor()
    try:
        cur.execute("SELECT codename FROM players WHERE id = %s;", (player_id,))
        result = cur.fetchone()
        if result:
            return result[0]  # Extract the codename from the tuple
    except psycopg2.Error as e:
        print("Error retrieving codename:", e)
    finally:
        cur.close()
        conn.close()

    return None  # Should not happen, since the function assumes the codename exists


def changeNetwork():
    def submitAddress():
        networkAddress = inputEntry.get().strip()  # Trim spaces

        # try to setIp if it fails its invalid
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

    inputButton = tk.Button(
        buttonFrame, text="Submit", command=submitAddress, bg="lightgreen"
    )
    inputButton.pack(side="left", padx=5)

    cancelButton = tk.Button(
        buttonFrame, text="Cancel", command=cancelInput, bg="#E36666"
    )
    cancelButton.pack(side="left", padx=5)

    errorLabel = tk.Label(inputFrame, text="", fg="red", width=40, anchor="center")
    errorLabel.grid(row=3, column=0, columnspan=2)


def getEquipmentId(
    entryNumber,
):  # prompts user for equipment id then adds it to the corresponding index in the equipmentIdList

    def submitEquipmentId():
        equipmentId = inputEntry.get()
        if len(equipmentId) == 2 and equipmentId.isdigit():
            equipmentIdList[entryNumber] = equipmentId
            print(equipmentIdList[entryNumber])
            inputWindow.destroy()
            udp.sendMessage(f"{equipmentId}")
            toggleMain(True)
        else:
            inputLabel.config(text="Invalid Equipment ID", fg="red")

    def cancelInput():
        inputWindow.destroy()
        playerIdList[entryNumber].config(state="normal")
        playerIdList[entryNumber].delete(0, tk.END)
        codenameList[entryNumber].delete(0, tk.END)
        toggleMain(True)

    inputWindow = tk.Toplevel(root)
    inputWindow.title("Input Equipment ID")
    inputWindow.geometry("300x200")
    inputWindow.minsize(300, 200)
    inputWindow.config(bg="lightblue")
    inputWindow.protocol("WM_DELETE_WINDOW", cancelInput)

    inputFrame = tk.Frame(inputWindow, padx=10, pady=10)
    inputFrame.place(x=75, y=50)

    inputLabel = tk.Label(inputFrame, text="Enter New Equipment ID:")
    inputLabel.grid(row=0, column=0)

    inputEntry = tk.Entry(inputFrame, width=20)
    inputEntry.grid(row=1, column=0)

    inputButton = tk.Button(
        inputFrame, text="Submit", command=submitEquipmentId, bg="lightgreen"
    )
    inputButton.grid(row=2, column=0)

    cancelButton = tk.Button(
        inputFrame, text="Cancel", command=cancelInput, bg="#E36666"
    )
    cancelButton.grid(row=3, column=0)


def characterCheck(codename):
    specialChars = r"!@#$%^&*()_+\-=\[\]{};\':\"\\|,.<>/?~"
    translationTable = str.maketrans("", "", specialChars)
    return codename.translate(translationTable) == codename

# Start server
def startUdpReceiveTask():
    def runUdp():
        asyncio.run(udp.startReceiver())

    threading.Thread(target=runUdp, daemon=True).start()

# Pre Game Error Checking for valid game
def preGameErrorCheck():
    # Makes sure there is at least 1 player on both teams
    redCount = 0
    greenCount = 0

    def makePlayerList():  # Add the contents of the 3 entry lists to the Player List
        nonlocal redCount, greenCount
        for i in range(30):
            playerId = playerIdList[i].get()
            codename = codenameList[i].get()
            equipmentId = equipmentIdList[i]

            # if the index of the current player is 0 - 14, red team. 15 - 29 is green team
            if equipmentId != "0" and i <= 14:
                playerList[i] = Player(playerId, codename, equipmentId, 0)
                redCount += 1
            elif equipmentId != "0" and 14 < i <= 29:
                playerList[i] = Player(playerId, codename, equipmentId, 1)
                greenCount += 1


    makePlayerList()

    if greenCount == 0 or redCount == 0:
        print("There must be a player on both teams to start")
        messagebox.showwarning(title="Error", message="There must be a player on both teams to start")
        return
    
    
    #remove player screen to show countdown
    for widget in root.winfo_children():
        if widget.winfo_name() == "playerScreen":
            widget.destroy()
    #Begin Countdown
    countDown(30)

# START GAME STUFF
def startGame():
    for i in range(30):
        if playerList[i] != None:
            print(
                f"{i}: {playerList[i].ID}, {playerList[i].Codename}, {playerList[i].EqpID}, {playerList[i].Team}"
            )

    startUdpReceiveTask()  # This works

    # Unbind bound keys
    root.unbind("<F5>")
    root.unbind("<F12>")

    # Start game loop
    print("Game started")
    gameMusic()

#counts down From Given Number then starts the game
def countDown(startingNumber=30):
    # Bypass countdown if "test" passed in
    if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        startGame()
    
    #get all numbers and sort them
    files = os.listdir("img/Numbers")
    files.sort()

    #turn the files into array of images for tk
    image_list = []
    for filename in files:
        img_path = os.path.join("img/Numbers", filename)
        image_list.append(ImageTk.PhotoImage(Image.open(img_path)))

    #if this is not here the images are Thrown Away
    root.image_list = image_list
    
    #get center of screen
    centerX = (root.winfo_width()) // 2
    centerY = (root.winfo_height()) // 2

    def complete():
        print("Countdown complete")
        startGame()
    #place on screen then remove
    def count(i, x):
        image_id = canvas.create_image(x, centerY, anchor="center", image=image_list[i])
        root.after((1000), lambda image_id: canvas.delete(image_id), image_id)

    #for 30 through 1 
    for i in range(startingNumber, 0, -1):
        numberOfDigits = len(str(i))
        #for each digit in number place on screen for 1 second then remove
        for j in range(numberOfDigits):
            x = (-(200*(numberOfDigits-1)/2) + (j*200) + centerX)
            root.after((startingNumber - i) * 1000, lambda i, x: count(i, x), int(str(i)[j]), x)

    root.after(startingNumber*1000, complete)

def handleRecieve(msg): 
    print(f"Processing message: {msg}")
    
    if ":" in msg:
        parts = msg.split(":")
        if len(parts) == 2:
            shooter, shot = parts  # Extract shooter and shot IDs
            actionLabelUpdate(shooter, shot)
            updateScore(shooter, shot)
            udp.sendMessage(shot)
        else:
            print("Invalid message format")
    else:
        print("Unrecognized message format")


def getPlayerFromEqpID(EqpID):
    for player in playerList:
        if player != None:
            if player.EqpID == EqpID:
                return player

def updateScore(shooterID, shotID):
    # get player from ID
    shooter = getPlayerFromEqpID(shooterID)
    if shotID != "43" and shotID != "53":
        shot = getPlayerFromEqpID(shotID)

    # Case 1: Shooter shot base
    if (shooter.Team == 0 and shotID == "43") or (shooter.Team == 1 and shotID == "53"):
        shooter.Score += 100
    # Case 2: Shooter shot opposite team
    elif (shooter.Team == 0 and shot.Team == 1) or (shooter.Team == 1 and shot.Team == 0):
        shooter.Score += 10
    # Case 3: Shooter shot same team
    elif shooter.Team == shot.Team and shooter.Score >= 0:
        shooter.Score -= 10 
    

def actionLabelUpdate(shooterID, shotID):
    # Shift labels up 1
    for i in range(len(actionList) - 1):
        actionList[i].config(text=actionList[i + 1].cget("text"))
    
    shooterName = "Unknown"
    shotName = "Unknown"

    # Retrieve codenames from IDs
    shooter = getPlayerFromEqpID(shooterID)
    shot = getPlayerFromEqpID(shotID)
    shooterName = shooter.Codename
    if shotID != "43" and shotID != "53":
        shotName = shot.Codename

    if shotID == "53":
        shotName = "the red base"
    if shotID == "43":
        shotName = "the green base"

    message = f"{shooterName} shot {shotName}"

    # Add new message to bottom
    actionList[14].config(text=message)





# Initialize ip/ports and send/receive sockets to starting values
udp = Udp("127.0.0.1", 7500, 7501)
udp.set_message_callback(handleRecieve)

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
redGameLabels = []
greenGameLabels = []
actionList = []
gameTime = 0

#will display splash image after startup then remove the image the show player screen
if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
    playerScreen()
else:
    root.after(1000, displaySplash)
    root.after(3000, lambda: canvas.delete("all"))
    root.after(3500, playerScreen)

# Run
root.mainloop()
