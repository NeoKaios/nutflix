from numpy import ndarray
from typing import Tuple
from abc import ABC, abstractmethod

class ABMarkInterface(ABC):
    @abstractmethod
    def createABImage(self, image: ndarray) -> Tuple[ndarray, ndarray]:
        pass

    @abstractmethod
    def readFrame(self, image: ndarray) -> int:
        pass

    @abstractmethod
    def getMethodName(self) -> str:
        pass

    def formatUsed(self) -> str:
        return 'rgb24'
