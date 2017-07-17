#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://71.68.222.92:80') as websocket:
        while True:
            test = await websocket.recv()
            print("<" + test)

asyncio.get_event_loop().run_until_complete(hello())
