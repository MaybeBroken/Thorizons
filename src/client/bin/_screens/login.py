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


def scr(
    render2d: None = None,
    aspect2d: None = None,
) -> NodePath:
    frame = DirectFrame(parent=render2d)
