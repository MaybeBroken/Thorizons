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


Keys = [
    ["ReactorTotalPower", 0],
    ["LeftGeneratorPowerIn", 0],
    ["RightGeneratorPowerIn", 0],
    ["LeftTransformer_1_Power", 0],
    ["RightTransformer_2_Power", 0],
    ["RightTransformer_1_Power", 0],
    ["LeftTransformer_2_Power", 0],
    ["ConnectedCard", "Shields", False, 0],
    ["ConnectedCard", "Generator", "LeftTransformer_1", False],
]


portNum = 8765


async def _echo(websocket):
    try:
        msg = await websocket.recv()
        encoder = js.encoder.JSONEncoder()
        decoder = js.decoder.JSONDecoder()
        if msg == ...:
            ...
    except:
        ...


async def _buildServe():
    async with websockets.serve(_echo, "localhost", int(portNum)):
        print(f"{'='*30}\nSERVER: listening on port {portNum}\n{'='*30}")
        await asyncio.Future()


Thread(target=asyncio.run, args=[_buildServe()]).start()

while True:
    t.sleep(2)