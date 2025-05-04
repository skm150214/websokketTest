import asyncio
import websockets

async def client():
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to server!")

            async def send_messages():
                while True:
                    # input() is blocking, so run it in a thread
                    msg = await asyncio.to_thread(input, "Enter message: ")
                    await websocket.send(msg)

            async def receive_messages():
                async for message in websocket:
                    #print(f"\nReceived from server: {message}")
                    break

            # Run both send and receive concurrently
            await asyncio.gather(send_messages(), receive_messages())

    except ConnectionRefusedError:
        print("Could not connect to server. Is it running?")
    except websockets.exceptions.ConnectionClosed:
        print("Disconnected from server.")

if __name__ == "__main__":
    asyncio.run(client())