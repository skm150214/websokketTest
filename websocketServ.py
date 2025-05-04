import asyncio
import websockets
#import pygame
#import sys
#from pathlib import Path
#pygame.init()
#pygame.font.init()
#clock = pygame.time.Clock()
#screen = pygame.display.set_mode((800,500))
#pygame.display.set_caption("konzola!!")
#THISFILE = Path(__file__).resolve().parent
#fontDir = THISFILE / "Tiny5-Regular.ttf"
#font = pygame.font.Font(str(fontDir), 40)

connected_clients = set()

async def handle(websocket):
    # Add new client to the set
    connected_clients.add(websocket)
    print(f"nov ljudek prišu v igro!!!!! koliko jih je zdej: {len(connected_clients)}")

    try:
        # Handle incoming messages from this client
        async for message in websocket:
            print(f"cli dal {message}")
            # Send message to all other clients
            others = connected_clients - {websocket}
            if others:
                await asyncio.gather(*(client.send(str(message)) for client in others))

    except websockets.exceptions.ConnectionClosed:
        print("Clientov internet je cooked :skull: .")

    finally:
        # Remove client from set when disconnected
        connected_clients.remove(websocket)
        print(f"Clienta no more D: še koliko ljudkov je tuki: {len(connected_clients)}")
## This assumes you're using websockets version 12.x or newer
#async def echo(connection):
#    #print("Client connected")
#    async for message in connection:
#        print(f"Received: {message}")
#        if len(message) > 0:await connection.send(message)

async def main():
    async with websockets.serve(handle, "localhost", 8765):
        print("Server running on ws://localhost:8765")        
        
        await asyncio.Future()  # Run forever

asyncio.run(main())

