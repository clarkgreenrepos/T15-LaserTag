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
import socket
import asyncio # this is the library necessary for async/await. https://docs.python.org/3/library/asyncio.html


def ValidPort(input: str) -> int:
    """Checks string if is a valid port and sends it back as an integer"""

    if not (input.isdigit()) or int(input) < 0 or int(input) > 65535:
        print("ERROR: Invalid Port '", input, "'")
        sys.exit(-1)  # On an Invalid Ip Exit
    return int(input)

async def udpServer(ip: str, port: int):
    """Asynchronous UDP server to receive player hit data."""
    loop = asyncio.get_running_loop()
    
    class UDPHandler(asyncio.DatagramProtocol):
        def datagram_received(self, data, addr):
            message = data.decode().strip()
            try:
                transmitting_id, hit_id = map(int, message.split(":"))
                print(f"{transmitting_id} : {hit_id}")
            except:
                """Any case where there is an invalid transmit/hit will be handled in udpSend.py"""

    print(f"Starting UDP server on {ip}:{port}")
    transport, protocol = await loop.create_datagram_endpoint(lambda: UDPHandler(), local_addr=(ip, port))
    print("Server is live\n")

    try:
        await asyncio.Event().wait()  # Server runs forever
    finally:
        transport.close()  # Close socket on exit

async def main():
    arguments = sys.argv[1:]
    
    ip = "127.0.0.1"  # Default IP.
    #TODO Add functionality to change IP addresses

    port = 7501       # receiving port

    if arguments:
        try:
            socket.inet_aton(arguments[0])
            ip = arguments[0]
        except socket.error:
            print("Error: Invalid IP")
            sys.exit(-1)
    
    if len(arguments) >= 2:
        port = ValidPort(arguments[1])

    server_task = asyncio.create_task(udpServer(ip, port))
    await server_task

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nUDP communication stopped.")
    

