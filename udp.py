import socket
import ipaddress
import asyncio


#I was dying copy and pasting between send/receive so I just put them both in a class.
class Udp:
    def __init__(self, ip="127.0.0.1", send_port=7501, recv_port=7500):
        """Initializes the UDP communication class."""
        self.ip = self.validate_ip(ip)
        self.send_port = self.validate_port(send_port)
        self.recv_port = self.validate_port(recv_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.transport = None
    
    #Check if IP is valid. Return ip if it is, return false and error if not
    def validate_ip(self, ip: str) -> str:
        """Validates and returns the given IP address."""
        ip = ip.strip()
        try:
            ipaddress.ip_address(ip)
            print(f"IP set to {ip}")
            return ip
        except ValueError:
            print(f"ERROR: Invalid IP '{ip}', using default 127.0.0.1")
            return "127.0.0.1"
        
    #Given a string checks if valid port and converts it to int
    def validate_port(this, input: str) -> int:
        """Checks string if is a valid port and sends it back as an integer"""
        # if the port is invalid the port is set to the default
        if not (input.isdigit()) or int(input) < 0 or int(input) > 65535:
            print("ERROR-udpSEND: Invalid Port '", input, "'")
            print("\tSetting To Default")
            return 7501 
        return int(input)

    #Given an int checks if valid port and returns it unchanged
    def validate_port(self, port: int) -> int:
        """Checks integer if is a valid port and sends it back as an integer"""
        if 0 <= port <= 65535:
            return port
        print(f"ERROR: Invalid Port '{port}', using default 7500")
        return 7501
    

    #Start receiving
    async def start_receiver(self):
        """Starts the UDP server to receive messages asynchronously."""
        loop = asyncio.get_running_loop()
        
        class UDPHandler(asyncio.DatagramProtocol):
            def datagram_received(self, data, addr):
                message = data.decode().strip()
                try:
                    transmitting_id, hit_id = map(int, message.split(":"))
                    print(f"Received: {transmitting_id} : {hit_id}")
                except ValueError:
                    print("Invalid message received.")
                    
        print(f"Starting UDP server on {self.ip}:{self.recv_port}")
        self.transport, _ = await loop.create_datagram_endpoint(
            lambda: UDPHandler(), local_addr=(self.ip, self.recv_port)
        )
        print("Server is live")

        try:
            await asyncio.Event().wait()
        finally:
            self.stop_receiver()


    #Stop receiving
    def stop_receiver(self):
        """Stops the UDP server."""
        if self.transport:
            self.transport.close()
            print("Server stopped.")


    # Given a message will send it to the server
    def send_message(self, message: str):
        """Sends a message over UDP."""
        msg_bytes = bytes(message, encoding="utf-8")
        self.sock.sendto(msg_bytes, (self.ip, self.send_port))

    # Not sure exactly how sending messages will look in it's true form so might as well keep it for now.
    def send_message(self, message: int):
        """Sends a message over UDP."""
        msg_bytes = bytes(message, encoding="utf-8")
        self.sock.sendto(msg_bytes, (self.ip, self.send_port))

    #Change/set IP
    def set_ip(self, new_ip: str):
        """Updates the IP address."""
        self.ip = self.validate_ip(new_ip)
    
    #Change/set Port for send or receiving sockets. Don't think changing port is necessary but it's I made it anyways.
    def set_send_port(self, new_port: int):
        """Updates the sending port."""
        self.send_port = self.validate_port(new_port)
    def set_recv_port(self, new_port: int):
        """Updates the receiving port."""
        self.recv_port = self.validate_port(new_port)

# Example usage
# udp_comm = UdpComm("127.0.0.1", 7501, 7500)
# asyncio.run(udp_comm.start_receiver())
# udp_comm.send_message("55:67")
