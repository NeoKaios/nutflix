from ab.watermarks.onepixel import ABMarkOnePixel
from ab.watermarks.qtyuv import ABMarkQTyuv
from ab.watermarks.blockpixel import ABMarkBlockPixel

def getWatermark(name):
    if(name=='1pix'):
        return ABMarkOnePixel()
    if(name=='blockP'):
        return ABMarkBlockPixel()
    if(name.startswith('qtyuv')):
        t=name[5:].split('#')
        return ABMarkQTyuv(int(t[0]),int(t[1]))
    return ABMarkQTyuv()

