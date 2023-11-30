import av
import av.container
from enum import Enum
from slash import slash

class PathType(str, Enum):
    MOVIE = f'movies{slash}'
    OUT = f'out{slash}'

def getFrames(container: av.container.Container):
    return container.decode(container.streams.video[0])

def getPackets(container: av.container.Container):
    return container.demux(container.streams.video[0])

def copyCodecContext(source: av.container.Container, destination: av.container.Container):
    # AUDIO ------------------
    # TODO
    # maybe only on server files?
    # audio_in = src.streams.audio[0]
    # audio_out = out.add_stream(audio_in.codec_context.name, 44100)

    video_in = source.streams.video[0]
    video_out = destination.add_stream(video_in.codec_context.name, '24')
    video_out.width = video_in.codec_context.width  # Set frame width to be the same as the width of the input audio_in
    video_out.height = video_in.codec_context.height  # Set frame height to be the same as the height of the input audio_in
    video_out.pix_fmt = video_in.codec_context.pix_fmt  # Copy pixel format from input audio_in to out audio_in
    video_out.options = {'crf': '23'}  # Select low crf for high quality (the price is larger file size).

