import av
from math import ceil,log2
import numpy as np
import os
from ab.container import *
from ab.watermarks.interface import ABMarkInterface
import matplotlib.pyplot as plt

nbUser = 1_000_000
nbBit = ceil(log2(nbUser)) # 20 for 10^6 users
nbFrameMarked = 48
treshold = nbFrameMarked * nbBit

def makeMarkedMovie(title: str, id: int, overwrite: bool = False) -> str:
    titleMarkedMovie = f'{title}-{id}'
    markedMovieExists = os.path.isfile(f'{PathType.OUT}{titleMarkedMovie}.mp4')
    if(markedMovieExists and not overwrite):
        print(f'Movie exists as {titleMarkedMovie}.mp4')
        return titleMarkedMovie

    # src = av.open(f'{PathType.OUT}{title}-A.mp4')
    # vid = src.streams.video[0]
    # print(vid.duration,vid.time_base)
    # for p in getPackets(src):
    #     print(p.pts,p.dts, sep='~',end='__')
    # print('ended')
    # src.close()
    movA = av.open(f'{PathType.OUT}{title}-A.mp4')
    movB = av.open(f'{PathType.OUT}{title}-B.mp4')
    markedMov = av.open(f'{PathType.OUT}{titleMarkedMovie}.mp4', 'w')

    video_in = movB.streams.video[0]
    markedMov.add_stream(template=video_in)
    vid = markedMov.streams.video[0]
    vid.time_base = movA.streams.video[0].time_base
    print('here----- ', movA.streams.video[0].time_base, vid.duration,vid.time_base)

    packetsA,packetsB = getPackets(movA),getPackets(movB)
    mark = None
    for idx,(packetA,packetB) in enumerate(zip(packetsA, packetsB)):
        if(idx%nbFrameMarked == 0):
            # print(packetA, packetB)
            print(f' {idx//24}s marked with {mark}')
            mark = id & 1
            id = id >> 1

        pack = packetA if mark==0 else packetB
        # if(mark==0):
        #     print('A', end='')
        #     pack = packetA
        # else:
        #     print('B', end='')
        #     pack = packetB
        # pack = packetA

        if pack.dts == None:
            continue
        pack.stream = markedMov.streams.video[0]
        markedMov.mux(pack)

    print(vid.duration,vid.time_base)
    markedMov.close()
    movA.close()
    movB.close()
    print(f'Movie written as {titleMarkedMovie}.mp4')
    return titleMarkedMovie


def markedMovieReader(title: str, mark: ABMarkInterface) -> int:
    print('Decoding '+title)
    src = av.open(f'{PathType.OUT}{title}.mp4')
    vid = src.streams.video[0]
    print(vid.duration,vid.time_base)
    for idx,p in enumerate(getPackets(src)):
        if(idx%nbFrameMarked == 0 and idx > 0):
            print(p.pts,p.dts, sep='~',end='__')
            # print('\n')
    print('ended')
    print('ended')
    print('ended')
    print('ended')
    print('ended')
    print('ended')
    src.close()

    src = av.open(f'{PathType.OUT}{title}.mp4')
    accBits = []
    readId = 0

    for idx,frame in enumerate(getFrames(src)):
        if(idx>treshold):
            continue
        image = frame.to_ndarray(format='rgb24')
        if(idx%nbFrameMarked == 0 and idx > 0):
            summed = sum(accBits)
            readBit = 0 if summed < nbFrameMarked/2 else 1
            print(frame.pts,frame.dts, sep='~',end='__')
            # print(f'\nCurrent val {frame.pts} {frame.dts}')
            print(f'{idx//24}s read {readBit} ({accBits.count(0)}/{accBits.count(1)})')

            readId += 2**(idx//nbFrameMarked - 1) * readBit

            # Start over for new bitgroup
            accBits = []

        bitFound = mark.readFrame(image)
        accBits.append(bitFound)

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
        image = frame.to_ndarray(format='rgb24')
        if(idx%nbFrameMarked == 0 and idx > 0):
            summed = sum(accBits)
            readBit = 0 if summed < nbFrameMarked/2 else 1
            # print(f'{idx//24}s read {readBit} ({accBits.count(0)}/{accBits.count(1)})')

            readId += 2**(idx//nbFrameMarked - 1) * readBit

            # Start over for new bitgroup
            accBits = []

        bitFound = mark.readFrame(image)
        accBits.append(bitFound)

    src.close()
    return readId

def slowmakeMarkedMovie(title: str, id: int, overwrite: bool = False) -> str:
    titleMarkedMovie = f'{title}-{id}'
    markedMovieExists = os.path.isfile(f'{PathType.OUT}{titleMarkedMovie}.mp4')
    if(markedMovieExists and not overwrite):
        print(f'Movie exists as {titleMarkedMovie}.mp4')
        return titleMarkedMovie

    movA = av.open(f'{PathType.OUT}{title}-A.mp4')
    movB = av.open(f'{PathType.OUT}{title}-B.mp4')

    markedMov = av.open(f'{PathType.OUT}{titleMarkedMovie}.mp4', 'w')
    copyCodecContext(movA, markedMov)

    framesA,framesB = getFrames(movA),getFrames(movB)
    mark = None
    for idx,(frameA,frameB) in enumerate(zip(framesA, framesB)):
        if(idx%nbFrameMarked == 0):
            print(f' {idx//24}s marked with {mark}')
            mark = id & 1
            id = id >> 1

        pack = frameA if mark==0 else frameB

        out_packet = markedMov.streams.video[0].encode(pack)  # Encode video frame
        markedMov.mux(out_packet)  # "Mux" the encoded frame (add the encoded frame to MP4 file).

    out_packet = markedMov.streams.video[0].encode(None)  # Encode video frame
    markedMov.mux(out_packet)  # "Mux" the encoded frame (add the encoded frame to MP4 file).

    markedMov.close()
    movA.close()
    movB.close()
    print(f'Movie written as {titleMarkedMovie}.mp4')
    return titleMarkedMovie

