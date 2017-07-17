#!/usr/bin/env python

import asyncio
import websockets

connected = set()

async def handler(websocket, path):
    global connected
    print(websocket)
    # Register
    connected.add(websocket)
    connected = True

    while connected:
        size = len(connected)
        try:
            # Implement logic here.
            print("Ping: " + str(size))
            await asyncio.wait([ws.send("Ping: " + str(size)) for ws in connected])
            await asyncio.sleep(15)
        except ConnectionClosed:
            connected = False
        except:
            raise
            
    connected.remove(websocket)

start_server = websockets.serve(handler, '10.0.1.77', 80, timeout=100) #put the server's local ip in here

asyncio.get_event_loop().run_until_complete(start_server)
print('Server started...')
asyncio.get_event_loop().run_forever()
