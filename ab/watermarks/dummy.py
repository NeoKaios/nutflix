from numpy import ndarray,flipud
from typing import Tuple
from ab.watermarks.interface import ABMarkInterface

class ABMarkDummy(ABMarkInterface):
    def createABImage(self, image: ndarray) -> Tuple[ndarray, ndarray]:
        return image, flipud(image)

    def readFrame(self, image: ndarray) -> int:
        return 0

    def getMethodName(self) -> str:
        return 'dummy'
