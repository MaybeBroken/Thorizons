from panda3d.core import (
    NodePath,
)
import opensimplex

min
opensimplex.seed(1234)


class generation:
    def __init__(
        self,
        noiseScale,
        noiseIntensity,
    ) -> None:

        # setup vars
        system = {
            "planets": None,
            "features": None,
            "": None,
        }
        x, y = 1, 1

        opensimplex.noise2(x * noiseScale, y * noiseScale)

        # TBD

        return system


class build:
    def __init__(self, world) -> None:
        rootNode = None
        itemDict = world

        # TBD

        return {"rootNode": rootNode, "itemDict": itemDict}
