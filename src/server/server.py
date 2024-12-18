from os import system

try:
    import websockets
except:
    system(f"python3 -m pip install websockets")
import time as t

try:
    import json as js
except:
    system(f"python3 -m pip install json")
import asyncio
from threading import Thread


Keys = {
    "reactor": {
        "energy": 0,
        "heat": 0,
        "stress": 0,
    },
    "shields": {
        "strength": 0,
        "stress": 0,
        "integrity": 0,
    },
    "weapons": {
        "lasers": {
            "stress": 0,
            "charge": 0,
            "heat": 0,
        },
        "torpedos": {
            "stress": 0,
            "charge": 0,
            "heat": 0,
            "ammo": {
                "large": 0,
                "small": 0,
            },
        },
    },
}

Internals = {
    "stations": {},
    "clients": [],
    "systemStress": {
        "ram": None,
        "cpu": None,
    },
}


portNum = 8765


async def _echo(websocket):
    try:
        msg = await websocket.recv()
        encoder = js.encoder.JSONEncoder()
        decoder = js.decoder.JSONDecoder()
        if msg == "requestMasterKeys":
            await websocket.send(encoder.encode(Keys))
        else:
            await websocket.send("unknown")
    except:
        print("client disconnected")


async def _buildServe():
    async with websockets.serve(_echo, "localhost", int(portNum)):
        print(f"{'='*30}\nSERVER: listening on port {portNum}\n{'='*30}")
        await asyncio.Future()


Thread(target=asyncio.run, args=[_buildServe()]).start()


while True:
    t.sleep(2)
