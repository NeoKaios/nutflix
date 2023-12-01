import numpy as np
from typing import Tuple
from ab.watermarks.interface import ABMarkInterface

class ABMarkBlockPixel(ABMarkInterface):
    def createABImage(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        imB = image.copy()
        for i in range(25):
            for j in range(25):
                image[i][j] = [0,0,200]
                imB[i][j] = [255, 255, 255]
        return image, imB

    def readFrame(self, image: np.ndarray) -> int:
        if(image[0][0].sum() > 127*3):
            return 1
        return 0

    def getMethodName(self) -> str:
        return 'blockP'
