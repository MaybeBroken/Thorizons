from panda3d.core import NodePath, loadPrcFile
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, DirectEntry, OnscreenText

loadPrcFile("src/client/bin/settings.prc")

def scr() -> NodePath:
    frame = NodePath('frame')

    b = DirectButton(parent=frame, text="Log-In", scale=0.1, pos=(-1, 0, -0.5))

    usr_entry = DirectEntry(parent=frame, scale=0.05, pos=(-0.5, 0, 0.001), numLines=1, width=10)
    usrnm = OnscreenText(parent=frame, scale=0.1, pos=(-1, 0, -0.1), text=("Username"))
    pswd = OnscreenText(parent=frame, scale=0.1, pos=(-1, -0.2, -0.1), text=("Password"))
    pswd_entry = DirectEntry(parent=frame, scale=0.05, pos=(-0.5, 0, -0.2), numLines=1, width=10, obscured=True)

    return frame


class Outline(ShowBase):
    def __init__(self):
        super().__init__()
        scr().reparentTo(self.aspect2d)



Outline().run()