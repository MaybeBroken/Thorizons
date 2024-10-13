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

try:
    from panda3d.core import *
except:
    system(f"python3 -m pip install panda3d")
from panda3d.core import TextNode, loadPrcFile, NodePath
from direct.showbase.ShowBase import ShowBase
from direct.stdpy.threading import Thread
from direct.gui.DirectGui import *

devMode = True

serverContents = []
portNum = 8765
if not devMode:
    ip = "wss://maybebroken.loca.lt"
else:
    ip = "ws://localhost:8765"

appGuiFrame = None
root3D = None


async def _send_recieve(data):
    async with websockets.connect(ip) as websocket:
        encoder = js.encoder.JSONEncoder()
        global serverContents, usrName, usrNameMenu, passwdMenu, auth
        if data == ...:
            ...
        else:
            # await websocket.send(encoder.encode(o=''))
            ...


def runClient(data):
    try:
        asyncio.run(_send_recieve(data))
    except:
        notify('network error')
        for i in range(5):
            try:
                asyncio.run(_send_recieve(data))
                break
            except:
                ...


class thorizons(ShowBase):
    def __init__(self, fStartDirect=True, windowType=None):
        super().__init__(fStartDirect, windowType)
        self.setupGuiInitial()
        self.setupControl()
    
    def setupControl(self):
        self.accept('q', exit)
        self.accept('1', runClient, extraArgs=['test'])

    def setupGuiInitial(self):
        global appGuiFrame, root3D
        self.root3D = NodePath(self.render)
        self.guiFrame = DirectFrame(parent=self.aspect2d)
        appGuiFrame = self.guiFrame
        root3D = self.root3D


def notify(message: str, pos=(0.8, 0, -0.5), scale=0.75):
    global appGuiFrame

    def fade(none):
        timeToFade = 20
        newMessage.setTransparency(True)

        def _internalThread():
            for i in range(timeToFade):
                val = 1 - (1 / timeToFade) * (i + 1)
                newMessage.setAlphaScale(val)
                t.sleep(0.01)
            newMessage.destroy()
            # newMessage.cleanup()

        Thread(target=_internalThread).start()

    newMessage = OkDialog(
        parent=appGuiFrame,
        text=message,
        pos=pos,
        scale=scale,
        frameColor=(0.5, 0.5, 0.5, 0.25),
        text_fg=(1, 1, 1, 1),
        command=fade,
        pad=[0.02, 0.02, 0.02, 0.02],
    )
    return newMessage


thorizons().run()
