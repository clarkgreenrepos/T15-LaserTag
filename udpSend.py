# UDP File

# Requirements
#   Need to set up 2 udp sockets for transmission of data to/from players
#   Use localhost (127.0.0.1) for network address
#   Use socket 7500 to broadcast, 7501 to receive
#   Include functionality to be able to change network address
#   Format of transmission will be a single integer (equipment id of player who got hit)
#   Format of received data will be integer:integer (equipment id of player transmitting:equipment id of player hit)

# Arguments
# 1st Message
# 2nd Custom Ip
# 3rd Custom Broadcast Port
# if any arguments are not given they will default to the value given in the requirements

import sys
import socket


def ValidPort(input: str) -> int:
    """Checks string if is a valid port and sends it back as an integer"""

    if not (input.isdigit()) or int(input) < 0 or int(input) > 65535:
        print("ERROR: Invalid Port '", input, "'")
        sys.exit(-1)  # On an Invalid Ip Exit
    return int(input)

def Send(message: str):
    """Sends A message over udp"""
    msgInBytes = bytes(message, encoding="utf-8")
    sock.sendto(msgInBytes, (ip, port))
    
def Send(message: int):
    """Sends A message over udp"""
    msgInBytes = bytes(message, encoding="utf-8")
    sock.sendto(msgInBytes, (ip, port))



arguments = sys.argv  # Arguments passed in
ip = "127.0.0.1"  # Default Ip Address
port = 7501  # Default  Port
message = "86" # Default Message

# Validation of Arguments

# removing the first argument because its the name of the file
arguments.pop(0)

# check for first argument [Custom Ip Address]
if len(arguments):
    message = arguments[0]
    
# check to see if first argument is a valid ip
if len(arguments) >= 2:
    try:
        socket.inet_aton(arguments[1])
        ip = arguments[1]
    except socket.error:
        print("ERROR: Invalid Ip")
        sys.exit(-1)  # On an Invalid Ip Exit

# check for second argument [Custom send Port]
if len(arguments) >= 3:
    port = ValidPort(arguments[2])



# create the socket for UDP
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# [DO NOT USE SEND BEFORE THIS POINT]


print("\nSending To:", ip, ":", port)

# Testing The UDP Function
Send(message)
