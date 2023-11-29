import av
from container import *

def makeMarkedMovie(title: str, id: int, watermarkingMethod: str) -> None:
    out = av.open(f'{PathType.OUT}{title}-{watermarkingMethod}-{id}.mp4', 'w')
    movA = av.open(f'{PathType.OUT}{title}-A.mp4')
    movB = av.open(f'{PathType.OUT}{title}-B.mp4')


    packetsA,packetsB = getPackets(movA),getPackets(movB)
    mark = None
    for idx,(packetA,packetB) in enumerate(zip(packetsA, packetsB)):
        if(idx%24 == 0):
            mark = id & 1
            id = id >> 1

        if(mark==0): # mark A
            pass
        else: # mark B
            pass


