import cv2
import itertools
import numpy as np
from typing import Tuple
from ab.watermarks.interface import ABMarkInterface
import random
import time

class RandomIter:
    def __init__(self, delta):
        self.delta = delta

    def __iter__(self):
      random.seed(789456123)
      return self

    def __next__(self):
        return random.random()*self.delta

class ABMarkQTyuv(ABMarkInterface):
    dct_coef = [1, 2, 3, 4, 8, 9, 10, 11, 16, 17, 18, 24]

    def __init__(self, delta=16,block_skip=8):
        self.delta = delta
        self.block_skip=block_skip

    def formatUsed(self):
        return 'yuv420p'

    def getIter(self, height, width):
        block_size = 8*self.block_skip
        return enumerate(itertools.product(range(0, height, block_size), range(0, width, block_size)))
        # return zip(range(10_000), itertools.product(range(0, height, 8), range(0, width, 8)))

    def createABImage(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        before = time.time()
        dithering = iter(RandomIter(self.delta))
        h = image.shape[0]
        w = image.shape[1]
        D = self.delta
        a=image
        b=image.copy()
        for _,(j,i) in self.getIter(h,w):
            dct = cv2.dct(image[j:j + 8, i:i + 8].astype(np.float32))
            dctb= dct.copy()
            for c in self.dct_coef:
                dith = dithering.__next__()
                dct[c//8,c%8] = D * round((dct[c//8,c%8] + dith)/D) - dith
                dctb[c//8,c%8] = D * round((dct[c//8,c%8] + dith + D/2)/D) - dith - D/2
                # *X[i] = delta * round( (*X[i] + d[i_m] + M[i_m] * delta/2) / delta) - d[i_m] - M[i_m] * delta/2;

            a[j:j+8,i:i+8] = cv2.idct(dct).astype(np.uint8)
            b[j:j+8,i:i+8] = cv2.idct(dctb).astype(np.uint8)
        # print(f"Time is {time.time()-before}")
        return a,b

    def readFrame(self, image: np.ndarray) -> int:
        before =time.time()
        dithering = iter(RandomIter(self.delta))
        h = image.shape[0]
        w = image.shape[1]
        D = self.delta
        m=[]
        for _,(j,i) in self.getIter(h,w):
            dct = cv2.dct(image[j:j + 8, i:i + 8].astype(np.float32))
            for c in self.dct_coef:
                dith = dithering.__next__()
                m += [int(abs(round((dct[c//8,c%8] + dith)/(D/2))))%2]
                # M[i_m] = (int)abs(round((*X[i] + d[i_m]) / (DELTA/2)))%2;
        # print(m.count(0)/(m.count(1)+m.count(0)))
        # print(f"time is {time.time()-before}")
        return 0 if m.count(0) > m.count(1) else 1

    def getMethodName(self) -> str:
        return f'qtyuv{self.delta}#{self.block_skip}'
