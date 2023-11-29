import numpy as np
from typing import Tuple
from interface import ABMarkInterface

class ABMarkOnePixel(ABMarkInterface):
    def createABImage(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        imB = image.copy()
        image[0][0] = [0,0,0]
        imB[0][0] = [255, 255, 255]
        return image, imB

    def readFrame(self, image: np.ndarray) -> int:
        if(image[0][0].sum() > 127*3):
            return 1
        return 0

    def getMethodName(self) -> str:
        return '1pix'
