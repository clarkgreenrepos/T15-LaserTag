#this file is useless right now, keeping it just in case.

class UdpReceive:
    #Initialize class
    def __init__(self, ip, port):
        self.ip = ip
        self.port = self.ValidPort(port)

    #Check if port is valid (between 0 and 65535)
    def ValidPort(self, port: int) -> int:
        """Checks if a port is valid and returns it as an integer."""
        if not (0 <= int(port) < 65535):
            print(f"ERROR: Invalid Port '{port}', setting port to default (7500)")
            self.ip = 7500
        return port
    
    def valid_ip(self, ip: str) -> str:
        ip = check_ip(ip)

    #Start the server
    async def start(self):
        """Starts the UDP server."""
        loop = asyncio.get_running_loop()
        
        class UDPHandler(asyncio.DatagramProtocol):
            def datagram_received(self, data, addr):
                message = data.decode().strip()
                try:
                    transmitting_id, hit_id = map(int, message.split(":"))
                    print(f"{transmitting_id} : {hit_id}")
                except ValueError:
                    pass 
        
        print(f"Starting UDP server on {self.ip}:{self.port}")
        self.transport, self.protocol = await loop.create_datagram_endpoint(
            lambda: UDPHandler(), local_addr=(self.ip, self.port)
        )
        print("Server is live\n")

        try:
            await asyncio.Event().wait() 
        finally:
            self.stop()

    #This will stop the server from listening
    def stop(self):
        """Stops the UDP server."""
        if self.transport:
            self.transport.close()
            print("Server stopped.")


    #Change port/ip with these methods
    def set_port(this, newPort: int):
        """sets the port"""
        this.port = this.ValidPort(newPort)
    def set_ip(this, newIp: str):
        """sets the Ip"""
        this.ip = check_ip(newIp)



    #Not sure if we'll need a restart method, but I added one just incase
    #(incase the server is listening, and the user changes the IP/Port)
    async def restart(self, new_ip=None, new_port=None):
        self.stop()
        if new_ip:
            self.ip = new_ip
        if new_port:
            self.port = new_port
        await self.start()


def check_ip(ip: str):
    try:
        socket.inet_aton(ip)
        return ip
    except socket.error:
        return "127.0.0.1"


#How to use:
#Start server-> server = UdpReceive("127.0.0.1", 7500)
#Stop server-> server.stop()
#Change port or ip -> server.setPort(int), server.setIp(str)