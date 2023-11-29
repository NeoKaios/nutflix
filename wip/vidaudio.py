import av
# from random import choice

src = av.open('movies/coca.mp4')
out = av.open('out/vid.mp4', 'w')

# AUDIO ------------------
audio_in = src.streams.audio[0]
audio_out = out.add_stream(audio_in.codec_context.name, 44100)

video_in = src.streams.video[0]
# fps = video_in.codec_context.rate  # Get the framerate from the input video audio_in.
video_out = out.add_stream(video_in.codec_context.name, '24')
# video_out = out.add_stream(template=video_in)
video_out.width = video_in.codec_context.width  # Set frame width to be the same as the width of the input audio_in
video_out.height = video_in.codec_context.height  # Set frame height to be the same as the height of the input audio_in
video_out.pix_fmt = video_in.codec_context.pix_fmt  # Copy pixel format from input audio_in to out audio_in
# video_out.options = {'crf': '23'}  # Select low crf for high quality (the price is larger file size).

src.seek(0)
for packet in src.demux((audio_in,)):
    # if packet.dts == None:
    #     continue
    for frame in packet.decode():
        a_frames = audio_out.encode(frame)
        out.mux(a_frames)
    # print(packet.dts)
    # packet.stream = video_out
    # out.mux(packet)

for pack in audio_out.encode(None):
    out.mux(pack)

# VIDEO ------------------

src.seek(0)
i=0
frames = src.decode(video_in)
for frame in frames:
    i+=1
    if(i%24==0 and i>0):
        print(f'Progress {i//24}s of {video_in.frames//24} s')

    out_frame = frame
    # if(i//24%2==1):
    #     arr = frame.to_ndarray()
    #     out_frame = av.VideoFrame.from_ndarray(arr, 'yuv420p')  # Note: to_image and from_image is not required in this specific example.
    print(frame.dts, frame.pts)
    out_packet = video_out.encode(out_frame)  # Encode video frame
    if(len(out_packet)>0):
        print(out_packet[0].pts)
        out_packet[0].dts+= 272 + i**2
        out_packet[0].pts =out_packet[0].dts
    out.mux(out_packet)  # "Mux" the encoded frame (add the encoded frame to MP4 file).

# Flush the encoder
out_packet = video_out.encode(None)
out.mux(out_packet)



src.close()
out.close()
