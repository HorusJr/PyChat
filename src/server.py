#!/usr/bin/env python

import asyncio
import websockets

connected = set()

async def handler(websocket, path):
    global connected
    # Register.
    connected.add(websocket)
    try:
        # Implement logic here.
        await asyncio.wait([ws.send("Hello!") for ws in connected])
        await asyncio.sleep(10)
    finally:
        # Unregister.
        connected.remove(websocket)

start_server = websockets.serve(hello, '10.0.1.77', 80) #put the server's local ip in here

asyncio.get_event_loop().run_until_complete(start_server)
print('Server started...')
asyncio.get_event_loop().run_forever()
