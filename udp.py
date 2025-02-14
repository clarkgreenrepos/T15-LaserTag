import socket
import ipaddress
import asyncio
import struct


# I was dying copy and pasting between send/receive so I just put them both in a class.
class Udp:
    def __init__(self, ip="127.0.0.1", sendPort=7500, receivePort=7501):
        """Initializes the UDP communication class."""
        self.setIp(ip)
        self.sendPort = self.validatePort(sendPort)
        self.receivePort = self.validatePort(receivePort)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.transport = None

    # Check if IP is valid. Return ip if it is, return false and error if not
    def validateIp(self, ip: str) -> bool:
        """determines if valid ip and returns Success bool"""
        ip = ip.strip()
        
        try: #check if ip is a valid ip
            ipaddress.ip_address(ip)
        except ValueError:
            print(f"ERROR: Invalid IP '{ip}', using {self.ip}")
            return 0
        #check if ip has been set before or if is equal to the newIp
        if(hasattr(self, "id") and self.ip == ip): 
            print(f"ERROR: IP is already '{self.ip}'")
            return 0
            
        print(f"'{ip}' valid")
        return 1


    # Given a string checks if valid port and converts it to int
    def validatePort(self, input: str) -> int:
        """Checks string if is a valid port and sends it back as an integer"""
        # if the port is invalid the port is set to the default
        if not (input.isdigit()) or int(input) < 0 or int(input) > 65535:
            print("ERROR-udpSEND: Invalid Port '", input, "'")
            print("\tSetting To Default")
            return 7501
        return int(input)

    # Given an int checks if valid port and returns it unchanged
    def validatePort(self, port: int) -> int:
        """Checks integer if is a valid port and sends it back as an integer"""
        if 0 <= port <= 65535:
            return port
        print(f"ERROR: Invalid Port '{port}', using default 7500")
        return 7501

    # Start receiving
    async def startReceiver(self):
        """Starts the UDP server to receive messages asynchronously."""
        loop = asyncio.get_running_loop()

        class UDPHandler(asyncio.DatagramProtocol):
            def datagram_received(self, data, addr):
                message = data.decode().strip()
                try:
                    transmittingId, hitId = map(int, message.split(":"))
                    print(f"Received: {transmittingId} : {hitId}")
                except ValueError:
                    print("Invalid message received.")

        print(f"Starting UDP server on {self.ip}:{self.receivePort}")
        self.transport, _ = await loop.create_datagram_endpoint(
            lambda: UDPHandler(), local_addr=(self.ip, self.receivePort)
        )
        print("Server is live")

        try:
            await asyncio.Event().wait()
        finally:
            self.stopReceiver()

    # Stop receiving
    def stopReceiver(self):
        """Stops the UDP server."""
        if self.transport:
            self.transport.close()
            print("Server stopped.")

    # Given a message will send it to the server
    def sendMessage(self, message: str):
        """Sends a message over UDP."""
        msgBytes = bytes(message, encoding="utf-8")
        self.sock.sendto(msgBytes, (self.ip, self.sendPort))
        print(
            f"Message sent from IP: {self.ip}, Port: {self.sendPort}, Message: {message}"
        )

    # Not sure exactly how sending messages will look in it's true form so might as well keep it for now.
    # def sendMessage(self, message: int):
    #     """Sends a message over UDP."""
    #     msgBytes = struct.pack('!I', message)
    #     self.sock.sendto(msgBytes, (self.ip, self.sendPort))
    #     print(f"Message sent from IP: {self.ip}, Port: {self.sendPort}, Message: {message}")

    # Change/set IP
    def setIp(self, newIp: str) -> bool:
        """Validates and Sets ip, Returns Success Bool"""
        if(self.validateIp(newIp)):
            self.ip = newIp.strip()
            return 1
        else:
            return 0
        

    # Change/set Port for send or receiving sockets. Don't think changing port is necessary but it's I made it anyways.
    def setSendPort(self, newPort: int):
        """Updates the sending port."""
        self.sendPort = self.validatePort(newPort)

    def setReceivePort(self, newPort: int):
        """Updates the receiving port."""
        self.receivePort = self.validatePort(newPort)

    def getIp(self):
        return self.ip


# Example usage
# udp = Udp("127.0.0.1", 7501, 7500)
# asyncio.run(udp.startReceiver())
# udp.sendMessage("55:67")
