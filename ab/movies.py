import os
import av
import av.container
from typing import List
from ab.watermarks.interface import ABMarkInterface
from ab.container import *

def setupABMoviesFiles(title: str, source_container: av.container.Container):
    movA = av.open(f'{PathType.OUT}{title}-A.mp4', 'w')
    movB = av.open(f'{PathType.OUT}{title}-B.mp4', 'w')

    # AUDIO ------------------
    # TODO
    # maybe only on server files?
    # audio_in = src.streams.audio[0]
    # audio_out = out.add_stream(audio_in.codec_context.name, 44100)

    copyCodecContext(source_container, movA)
    copyCodecContext(source_container, movB)

    return movA, movB

def createABMovies(title: str, mark: ABMarkInterface, overwrite: bool = False):
    titleAndMethod = title + '-' + mark.getMethodName()
    movieAExists = os.path.isfile(f'{PathType.OUT}{titleAndMethod}-A.mp4')
    movieBExists = os.path.isfile(f'{PathType.OUT}{titleAndMethod}-B.mp4')
    if(not overwrite and movieAExists and movieBExists):
        return

    src = av.open(f'{PathType.MOVIE}{title}.mp4')

    movA, movB = setupABMoviesFiles(titleAndMethod, src)

    frames = getFrames(src)

    for frame in frames:
        # Create A/B frames
        image = frame.to_ndarray(format='rgb24')
        imageA,imageB = mark.createABImage(image)
        # Encode frame in file
        for (imageX,movX) in [(imageA,movA),(imageB, movB)]:
            frameX = av.VideoFrame.from_ndarray(imageX, 'rgb24')
            packetX = movX.streams.video[0].encode(frameX)
            movX.mux(packetX)

    # Flush buffers
    packetA = movA.streams.video[0].encode(None)
    movA.mux(packetA)
    packetB = movB.streams.video[0].encode(None)
    movB.mux(packetB)

    src.close()
    movA.close()
    movB.close()

def createABLibrary(movieList: List[str], mark: ABMarkInterface):
    for title in movieList:
        createABMovies(title, mark)

