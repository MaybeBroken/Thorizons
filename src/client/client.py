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
try:
    from screeninfo import get_monitors
except:
    system(f"python3 -m pip install screeninfo")
import asyncio

try:
    from panda3d.core import *
except:
    system(f"python3 -m pip install panda3d")
from panda3d.core import TextNode, loadPrcFile, NodePath, WindowProperties
from direct.showbase.ShowBase import ShowBase
from direct.stdpy.threading import Thread
from direct.gui.DirectGui import *

from bin.colors import _dict as Color


monitor = get_monitors()[0]
screenX = monitor.width
screenY = monitor.height
aspectX = screenY / screenX
aspectY = screenX / screenY
devMode = True
serverContents = []
portNum = 8765
root3D = None
appGuiFrame = None

loadPrcFile("bin/settings.prc")

if not devMode:
    ip = "wss://maybebroken.loca.lt"
else:
    ip = "ws://localhost:8765"


def ColToScalar(val):
    return val / 255


def RgbToScalar(r, g, b, a) -> tuple[4]:
    return (ColToScalar(r), ColToScalar(g), ColToScalar(b), a)


def decrypt(data):
    print(data)


async def _send_recieve(data):
    async with websockets.connect(ip) as websocket:
        encoder = js.encoder.JSONEncoder()
        decoder = js.decoder.JSONDecoder()
        global serverContents, usrName, usrNameMenu, passwdMenu, auth
        if data == "requestMasterKeys":
            await websocket.send(data)
            decrypt(decoder.decode(await websocket.recv()))
        else:
            await websocket.send(encoder.encode(data))
            decrypt(decoder.decode(await websocket.recv()))


def runClient(data):
    try:
        asyncio.run(_send_recieve(data))
    except:
        notify("network error")
        for i in range(5):
            try:
                asyncio.run(_send_recieve(data))
                break
            except:
                ...


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


class thorizons(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()
        self.setupGuiFrames()
        self.setupControl()
        self.setup3D()
        self.loginScreen()
        # print(self.getScreenSize())

    def getScreenSize(self):
        props = WindowProperties()
        return props.getSize()

    def setScreenSize(self, w, h):
        props = WindowProperties()
        props.setSize(w, h)
        self.win.requestProperties(props)

    def setupControl(self):
        self.accept("q", exit)
        self.accept("n", notify, ["test alert"])
        self.accept("s", runClient, ["requestMasterKeys"])
    
    def updateCursorItemsPos(self, task):
        return task.cont

    def setupGuiFrames(self):
        global appGuiFrame, root3D
        self.root3D = NodePath(self.render)
        self.guiFrame = DirectFrame(parent=self.render2d)
        appGuiFrame = self.guiFrame
        root3D = self.root3D
        self.backgroundObjNode = NodePath("backgroundModel")
        self.backgroundObjNode.reparentTo(self.render)
        self.backgroundObj1 = self.loader.loadModel("data/models/skybox/stars.egg")
        self.backgroundObj1.reparentTo(self.backgroundObjNode)
        self.backgroundObj1.setScale(50)
        self.backgroundObj2 = self.loader.loadModel("data/models/skybox/stars.egg")
        self.backgroundObj2.reparentTo(self.backgroundObjNode)
        self.backgroundObj2.setScale(50)
        self.backgroundObj2.setR(180)
        self.taskMgr.add(self.updateCursorItemsPos)

    def loginScreen(self): ...
    def opsScreen(self): ...
    def flightScreen(self): ...
    def XOScreen(self): ...
    def commScreen(self): ...
    def weaponsScreen(self): ...
    def viewScreen(self): ...
    def setup3D(self): ...


thorizons().run()
