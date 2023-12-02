import cv2
import itertools
import numpy as np
from typing import Tuple
from ab.watermarks.interface import ABMarkInterface

class ABMarkQT(ABMarkInterface):
    dct_coef = [1, 2, 3, 4, 8, 9, 10, 11, 16, 17, 18, 24]
    # dct_coef = [1, 2, 3, 4, 8]
    delta = 8
    def getIter(self, height, width):
        return zip(range(300_000), itertools.product(range(0, height//2, 8), range(0, width//2, 8)))
        # return zip(range(10_000), itertools.product(range(0, height, 8), range(0, width, 8)))

    def write(self, bit, image: np.ndarray) -> np.ndarray:
        h = image.shape[0]
        w = image.shape[1]
        D = self.delta
        img_blocks =[image[j:j + 8, i:i + 8] for _,(j,i) in self.getIter(h,w)]
        # dct = [cv2.dct(img_block) for img_block in img_blocks]

        for idx,block in enumerate(img_blocks):
            dct = cv2.dct(block)
            for c in self.dct_coef:
                dith = 0 # random()
                dct[c//8,c%8] = D * round((dct[c//8,c%8] + dith + bit*D/2)/D) - dith - bit*D/2
                # *X[i] = delta * round( (*X[i] + d[i_m] + M[i_m] * delta/2) / delta) - d[i_m] - M[i_m] * delta/2;
            img_blocks[idx] = cv2.idct(dct)
        for idx,(j,i) in self.getIter(h,w):
            image[j:j+8,i:i+8] = img_blocks[idx]
        return image


    def createABImage(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        b = image.copy()
        reda = image[:,:,0].astype(np.float32)
        redb = b[:,:,0].astype(np.float32)
        image[:,:,0] = self.write(0,reda).astype(np.uint8)
        b[:,:,0] = self.write(1,redb).astype(np.uint8)
        return image,b

    def readFrame(self, image: np.ndarray) -> int:
        h = image.shape[0]
        w = image.shape[1]
        r = image[:,:,0].astype(np.float32)
        D = self.delta
        img_blocks =[r[j:j + 8, i:i + 8] for _,(j,i) in self.getIter(h,w)]
        dct = [cv2.dct(img_block) for img_block in img_blocks]
        m=[]
        for block in dct:
            for c in self.dct_coef:
                dith = 0 # random()
                m += [int(abs(round((block[c//8,c%8] + dith)/(D/2))))%2]
                # M[i_m] = (int)abs(round((*X[i] + d[i_m]) / (DELTA/2)))%2;
        print(m.count(0))
        print(m.count(1))
        return 0 if m.count(0) > m.count(1) else 1

    def getMethodName(self) -> str:
        return f'qt{self.delta}'

if __name__ == "__main__":
    m = ABMarkQT();
    im = np.ones((100,100,3));
    print(im)
    print(cv2.dct(im))

#input is a RGB numpy array with shape (height,width,3), can be uint,int, float or double, values expected in the range 0..255
#output is a double YUV numpy array with shape (height,width,3), values in the range 0..255
def RGB2YUV( rgb ):

    m = np.array([[ 0.29900, -0.16874,  0.50000],
                 [0.58700, -0.33126, -0.41869],
                 [ 0.11400, 0.50000, -0.08131]])

    yuv = np.dot(rgb,m)
    yuv[:,:,1:]+=128.0
    return yuv

#input is an YUV numpy array with shape (height,width,3) can be uint,int, float or double,  values expected in the range 0..255
#output is a double RGB numpy array with shape (height,width,3), values in the range 0..255
def YUV2RGB( yuv ):

    m = np.array([[ 1.0, 1.0, 1.0],
                 [-0.000007154783816076815, -0.3441331386566162, 1.7720025777816772],
                 [ 1.4019975662231445, -0.7141380310058594 , 0.00001542569043522235] ])

    rgb = np.dot(yuv,m)
    rgb[:,:,0]-=179.45477266423404
    rgb[:,:,1]+=135.45870971679688
    rgb[:,:,2]-=226.8183044444304
    return rgb
