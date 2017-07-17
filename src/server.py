#!/usr/bin/env python

import asyncio
import websockets
import logging

clients = {}

async def handler(websocket, path):
    print('New client', websocket)
    print(' ({} existing clients)'.format(len(clients)))

    # first line from client is client name
    name = await websocket.recv()
    await websocket.send('Welcome to the chatroom, {}'.format(name))
    await websocket.send('Users: {}'.format(list(clients.values())))
    clients[websocket] = name
    for client, _ in clients.items():
        await client.send(name + ' has joined the chat')

    while True:
        message = await websocket.recv()
        if message is None:
            their_name = clients[websocket]
            del clients[websocket]
            print('Client closed connection', websocket)

            for client, _ in clients.items():
                await client.send(their_name + ' has let the chat')
            break

        for client, _ in clients.items():
            await client.send('{}: {}'.format(name, message))

start_server = websockets.serve(handler, 'localhost', 3000, timeout=100) #put the server's local ip in here

asyncio.get_event_loop().run_until_complete(start_server)
print('Server started')
asyncio.get_event_loop().run_forever()
