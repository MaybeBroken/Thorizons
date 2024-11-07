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
from panda3d.core import (
    TextNode,
    loadPrcFile,
    NodePath,
    WindowProperties,
    ConfigVariableString,
)
from direct.showbase.ShowBase import ShowBase
from direct.stdpy.threading import Thread
from direct.gui.DirectGui import *

from bin.colors import _dict as Color
from bin.physics import physicsMgr

monitor = get_monitors()
screenX = monitor[0].width
screenY = monitor[0].height
aspectX = screenY / screenX
aspectY = screenX / screenY
devMode = True
serverContents = []
portNum = 8765
root3D = None
appGuiFrame = None

loadPrcFile("bin/settings.prc")
ConfigVariableString(
    "win-size", str(monitor[0].width) + " " + str(monitor[0].height)
).setValue(str(monitor[0].width) + " " + str(monitor[0].height))


monitor = get_monitors()


ConfigVariableString("win-size", str(screenX) + " " + str(screenY)).setValue(
    str(screenX) + " " + str(screenY)
)
ConfigVariableString("fullscreen", "false").setValue("false")
ConfigVariableString("undecorated", "true").setValue("true")


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
        physicsMgr.enable(physicsMgr, gravity=(0, 0, 0))
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
        self.accept("n", notify, ["test alert long message idk"])
        self.accept("s", runClient, ["requestMasterKeys"])

    def update(self, task):
        physicsMgr.updateWorldPositions(physicsMgr)
        result = task.cont
        dt = globalClock.getDt()  # type: ignore
        self.cameraSwingFactor = 0.6

        # x_movement = 0
        # y_movement = 0
        # z_movement = 0

        # if self.keyMap["forward"]:
        #     x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        #     y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        # if self.keyMap["backward"]:
        #     x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        #     y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        # if self.keyMap["left"]:
        #     x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        #     y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        # if self.keyMap["right"]:
        #     x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        #     y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        # if self.keyMap["up"]:
        #     z_movement += dt * playerMoveSpeed
        # if self.keyMap["down"]:
        #     z_movement -= dt * playerMoveSpeed

        # self.camera.setPos(
        #     self.camera.getX() + x_movement,
        #     self.camera.getY() + y_movement,
        #     self.camera.getZ() + z_movement,
        # )
        # Wvars.camX = self.camera.getX()
        # Wvars.camY = self.camera.getY()
        # Wvars.camZ = self.camera.getZ()

        md = self.win.getPointer(0)
        mouseX = md.getX()
        mouseY = md.getY()

        # if int(monitor[0].width / 2) - mouseX >= int(monitor[0].width / 4):
        #     self.win.movePointer(0, x=int(monitor[0].width / 2), y=int(mouseY))
        #     self.lastMouseX = int(monitor[0].width / 2)
        # elif int(monitor[0].width / 2) - mouseX <= -int(monitor[0].width / 4):
        #     self.win.movePointer(0, x=int(monitor[0].width / 2), y=int(mouseY))
        #     self.lastMouseX = int(monitor[0].width / 2)
        # elif int(monitor[0].height / 2) - mouseY >= int(monitor[0].height / 4):
        #     self.win.movePointer(0, x=int(mouseX), y=int(monitor[0].height / 2))
        #     self.lastMouseY = int(monitor[0].height / 2)
        # elif int(monitor[0].height / 2) - mouseY <= -int(monitor[0].height / 4):
        #     self.win.movePointer(0, x=int(mouseX), y=int(monitor[0].height / 2))
        #     self.lastMouseY = int(monitor[0].height / 2)

        # else:
        mouseChangeX = mouseX - self.lastMouseX
        mouseChangeY = mouseY - self.lastMouseY

        currentH = self.camera.getH()
        currentP = self.camera.getP()
        currentR = self.camera.getR()

        self.camera.setHpr(
            currentH - mouseChangeX * dt * self.cameraSwingFactor,
            min(
                45, max(-45, currentP - mouseChangeY * dt * self.cameraSwingFactor)
            ),
            0,
        )

        self.lastMouseX = mouseX
        self.lastMouseY = mouseY
        # if Wvars.inInventory == True:
        #     md = self.win.getPointer(0)
        #     self.lastMouseX = md.getX()
        #     self.lastMouseY = md.getY()
        return result

    def setupGuiFrames(self):
        global appGuiFrame, root3D
        self.root3D = NodePath(self.render)
        self.guiFrame = DirectFrame(parent=self.aspect2d)
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
        self.lastMouseX = self.win.getPointer(0).getX()
        self.lastMouseY = self.win.getPointer(0).getX()
        self.hideCursor(False)
        self.taskMgr.add(self.update)

    def hideCursor(self, boolVar):
        properties = WindowProperties()
        properties.setCursorHidden(boolVar)
        properties.setMouseMode(WindowProperties.M_relative)
        self.win.requestProperties(properties)

    def loginScreen(self): ...
    def opsScreen(self): ...
    def flightScreen(self): ...
    def XOScreen(self): ...
    def commScreen(self): ...
    def weaponsScreen(self): ...
    def viewScreen(self): ...

    def setup3D(self): ...

thorizons().run()
