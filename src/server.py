#!/usr/bin/env python

import asyncio
import websockets

async def hello(websocket, path):
    name = await websocket.recv()
    print("< {}".format(name))

    greeting = "Hello {}!".format(name)
    await websocket.send(greeting)
    print("> {}".format(greeting))

start_server = websockets.serve(hello, '10.0.1.77', 80) #put the server's local ip in here

asyncio.get_event_loop().run_until_complete(start_server)
print('Server started...')
asyncio.get_event_loop().run_forever()