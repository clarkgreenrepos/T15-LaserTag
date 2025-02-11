# UDP Send File

import socket

#The UDP Class sends messages to any UDP Server
class UdpSend:
    """The Class For Send Messages Over UDP"""
    #Initializer, allows you to set a different ip or port
    def __init__(this, ip: str = "127.0.0.1", port: str = "7501"):
        """sets the ip and port and creates the socket"""
        this.setIp(ip) #set the ip
        this.setPort(port) # set the port
        
        #create the socket
        this.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    #Given a string checks if valid port and converts it to int
    def ValidPort(this, input: str) -> int:
        """Checks string if is a valid port and sends it back as an integer"""
        # if the port is invalid the port is set to the default
        if not (input.isdigit()) or int(input) < 0 or int(input) > 65535:
            print("ERROR: Invalid Port '", input, "'")
            print("\tSetting To Default")
            return 7501 
        return int(input)

    #Given an int checks if valid port and returns it unchanged
    def ValidPort(this, input: int) -> int:
        """Checks string if is a valid port and sends it back as an integer"""
        # if the port is invalid the port is set to the default
        if input < 0 or input > 65535:
            print("ERROR: Invalid Port '", input, "'")
            print("\tSetting To Default")
            return 7501
        return input

    #the Main function for this class
    # Given a message will send it to the server
    def Send(this, message: str):
        """Sends A message over udp"""
        msgInBytes = bytes(message, encoding="utf-8")
        this.sock.sendto(msgInBytes, (this.ip, this.port))

    # same as the other one but for int (Probably redundant)
    def Send(this, message: int):
        """Sends A message over udp"""
        msgInBytes = bytes(message, encoding="utf-8")
        this.sock.sendto(msgInBytes, (this.ip, this.port))
    
    #sets the port and checks if valid
    def setPort(this, newPort: str):
        """sets the port"""
        this.port = this.ValidPort(newPort)
    def setPort(this, newPort: int):
        """sets the port"""
        this.port = this.ValidPort(newPort)
     #sets the ip and checks if valid
    def setIp(this, newIp: str):
        """sets the Ip"""
        try:
            socket.inet_aton(newIp)
            this.ip = newIp
        except socket.error:
            print("ERROR: Invalid Ip")
            print("\tSetting To Default")
            this.ip = "127.0.0.1"


#EXAMPLE on how to use the class
# udp = UdpSend("127.0.0.1", 7501)
# udp.Send("55:67")
