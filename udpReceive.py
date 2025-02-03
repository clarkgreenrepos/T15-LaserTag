# UDP File

# Requirements
#   Need to set up 2 udp sockets for transmission of data to/from players
#   Use localhost (127.0.0.1) for network address
#   Use socket 7500 to broadcast, 7501 to receive
#   Include functionality to be able to change network address
#   Format of transmission will be a single integer (equipment id of player who got hit)
#   Format of received data will be integer:integer (equipment id of player transmitting:equipment id of player hit)

# Arguments
# 1st Custom Ip
# 2nd Custom Port
# if any arguments are not given they will default to the value given in the requirements

import sys
import os
import socket


def ValidPort(input: str) -> int:
    """Checks string if is a valid port and sends it back as an integer"""

    if not (input.isdigit()) or int(input) < 0 or int(input) > 65535:
        print("ERROR: Invalid Port '", input, "'")
        sys.exit(-1)  # On an Invalid Ip Exit
    return int(input)


arguments = sys.argv  # Arguments passed in
ip = "127.0.0.1"  # Default Ip Address
port = 7501  # Default Sending Port


print(arguments)

# Validation of Arguments

# removing the first argument because its the name of the file
arguments.pop(0)

# check for first argument [Custom Ip Address]
if len(arguments):
    # check to see if first argument is a valid ip
    try:
        socket.inet_aton(arguments[0])
        ip = arguments[0]
    except socket.error:
        print("ERROR: Invalid Ip")
        sys.exit(-1)  # On an Invalid Ip Exit

# check for second argument [Custom Receive Port]
if len(arguments) >= 2:
    port = ValidPort(arguments[1])

# create the socket for UDP
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

print("\nSending To:", ip, ":", port)
print("Receiving From Port:", port, "\n")

# Testing The UDP Function

sock.bind((ip, port))


# main loop [Activates on message Received]
while(True):
    bytesAddressPair = sock.recvfrom(1024)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)
    

