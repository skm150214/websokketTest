import asyncio
import websockets

# This assumes you're using websockets version 12.x or newer
async def echo(connection):
    #print("Client connected")
    async for message in connection:
        print(f"Received: {message}")
        if len(message) > 0:await connection.send(message)

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        print("Server running on ws://localhost:8765")
        
        #exec(input("Send arbitrary message:"))
        await asyncio.Future()  # Run forever

asyncio.run(main())