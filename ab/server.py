import av
from container import *

def makeMarkedMovie(title: str, id: int) -> None:
    movA = av.open(f'{PathType.OUT}{title}-A.mp4')
    movB = av.open(f'{PathType.OUT}{title}-B.mp4')
    markedMov = av.open(f'{PathType.OUT}{title}-{id}.mp4', 'w')

    video_in = movB.streams.video[0]
    markedMov.add_stream(template=video_in)

    packetsA,packetsB = getPackets(movA),getPackets(movB)
    mark = None
    for idx,(packetA,packetB) in enumerate(zip(packetsA, packetsB)):
        if(idx%24 == 0):
            print(f'{idx//24}s marked')
            mark = id & 1
            id = id >> 1

        pack = packetA if mark==0 else packetB
        # pack = packetA

        if pack.dts == None:
            continue
        pack.stream = markedMov.streams.video[0]
        markedMov.mux(pack)

    markedMov.close()
    movA.close()
    movB.close()


