#!/usr/bin/env python

import asyncio
import websockets

connected = set()

async def handler(websocket, path):
    global connected
    print(websocket)
    # Register
    connected.add(websocket)
    size = len(s)

    while True:
        try:
            # Implement logic here.
            await asyncio.wait([ws.send("Ping: " + size) for ws in connected])
            await asyncio.sleep(15)
        finally:
            print("next")

    connected.remove(websocket)

start_server = websockets.serve(handler, '10.0.1.77', 80, timeout=100) #put the server's local ip in here

asyncio.get_event_loop().run_until_complete(start_server)
print('Server started...')
asyncio.get_event_loop().run_forever()
