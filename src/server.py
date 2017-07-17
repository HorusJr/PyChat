#!/usr/bin/env python

import asyncio
import websockets

connections = set()

async def handler(websocket, path):
    global connected
    print(websocket)
    # Register
    connections.add(websocket)
    connected = True

    while connected:
        size = len(connections)
        try:
            # Implement logic here.
            print("Ping: " + str(size))
            await asyncio.wait([ws.send("Ping: " + str(size)) for ws in connections])
            await asyncio.sleep(5)
        except websockets.exceptions.ConnectionClosed as e:
            print("EXCEPTION!!!")
            connected = False
        except:
            raise

    connected.remove(websocket)

start_server = websockets.serve(handler, 'localhost', 3000, timeout=100) #put the server's local ip in here

asyncio.get_event_loop().run_until_complete(start_server)
print('Server started')
asyncio.get_event_loop().run_forever()
