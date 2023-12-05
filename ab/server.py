import av
from math import ceil,log2
import os
from ab.container import *
from ab.watermarks.interface import ABMarkInterface

nbUser = 1_000_000
nbBit = ceil(log2(nbUser)) # 20 for 10^6 users
nbFrameMarked = 24
treshold = nbFrameMarked * nbBit

def makeMarkedMovie(title: str, id: int, overwrite: bool = False) -> str:
    id %= nbUser
    titleMarkedMovie = f'{title}-{id}'
    markedMovieExists = os.path.isfile(f'{PathType.OUT}{titleMarkedMovie}.mp4')
    if(markedMovieExists and not overwrite):
        print(f'Movie exists as {titleMarkedMovie}.mp4')
        return titleMarkedMovie

    movA = av.open(f'{PathType.OUT}{title}-A.mp4')
    movB = av.open(f'{PathType.OUT}{title}-B.mp4')
    markedMov = av.open(f'{PathType.OUT}{titleMarkedMovie}.mp4', 'w')

    video_in = movB.streams.video[0]
    video_out = markedMov.add_stream(template=video_in)
    video_out.options = {'x264-params': 'keyint=24:min-keyint=24:scenecut=0' }  # Select low crf for high quality (the price is larger file size).

    packetsA,packetsB = getPackets(movA),getPackets(movB)
    mark = None
    for idx,(packetA,packetB) in enumerate(zip(packetsA, packetsB)):
        if(idx%nbFrameMarked == 0):
            print(f' {idx//24}s marked with {mark}')
            mark = id & 1
            id = id >> 1

        pack = packetA if mark==0 else packetB

        if pack.dts == None:
            continue
        pack.stream = video_out
        markedMov.mux(pack)

    markedMov.close()
    movA.close()
    movB.close()
    print(f'Movie written as {titleMarkedMovie}.mp4')
    return titleMarkedMovie

def markedMovieReader(title: str, mark: ABMarkInterface) -> int:
    print('Decoding '+title)

    src = av.open(f'{PathType.OUT}{title}.mp4')
    accBits = []
    readId = 0

    ptss = [0]
    sho = []
    i=0
    for idx,frame in enumerate(getFrames(src)):
        i=idx
        if(idx>treshold):
            continue
        sho+=[frame.pts - ptss[-1]]
        ptss+=[frame.pts]
        image = frame.to_ndarray(format=mark.formatUsed())
        if(idx%nbFrameMarked == 0 and idx > 0):
            summed = sum(accBits)
            readBit = 0 if summed < nbFrameMarked/2 else 1
            # print(frame.pts,frame.dts, sep='~',end='__')
            # print(f'\nCurrent val {frame.pts} {frame.dts}')
            print(accBits)
            print(f'{idx//24}s read {readBit} ({accBits.count(0)}/{accBits.count(1)})')

            readId += 2**(idx//nbFrameMarked - 1) * readBit

            # Start over for new bitgroup
            accBits = []

        bitFound = mark.readFrame(image)
        accBits.append(bitFound)

    print("nb frames:", i)
    summed = sum(accBits)
    readBit = 0 if summed < nbFrameMarked/2 else 1
    print(f'extra  read {readBit} ({accBits.count(0)}/{accBits.count(1)})')
    src.close()
    return readId


def markedMovieReaderLogless(title: str, mark: ABMarkInterface) -> int:
    src = av.open(f'{PathType.OUT}{title}.mp4')
    accBits = []
    readId = 0

    for idx,frame in enumerate(getFrames(src)):
        if(idx>treshold):
            continue
        image = frame.to_ndarray(format=mark.formatUsed())
        if(idx%nbFrameMarked == 0 and idx > 0):
            summed = sum(accBits)
            readBit = 0 if summed < nbFrameMarked/2 else 1
            readId += 2**(idx//nbFrameMarked - 1) * readBit

            # Start over for new bitgroup
            accBits = []

        bitFound = mark.readFrame(image)
        accBits.append(bitFound)

    src.close()
    return readId
