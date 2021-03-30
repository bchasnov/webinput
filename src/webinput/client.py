import asyncio
import websockets
import json

async def client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # Allow user to enter username into command line
        while True:
            response = await websocket.recv()
            print(response)
        
asyncio.get_event_loop().run_until_complete(client())
