import av

src = av.open('movies/coca.mp4')
# src = av.open('out/vid.mp4')
out = av.open('out/vid.mp4', 'w')

video_in = src.streams.video[0]
# out_stream = out.add_stream(template=video_in)  # Using template=video_in is not working (probably meant to be used for re-muxing and not for re-encoding).

codec_name = video_in.codec_context.name  # Get the codec name from the input video stream.
fps = video_in.codec_context.rate  # Get the framerate from the input video stream.
video_out = out.add_stream(codec_name, '24')
# video_out = out.add_stream(template=video_in)

# video_out = video_in.codec_context  # Set frame width to be the same as the width of the input stream
video_out.width = video_in.codec_context.width  # Set frame width to be the same as the width of the input stream
video_out.height = video_in.codec_context.height  # Set frame height to be the same as the height of the input stream
video_out.pix_fmt = video_in.codec_context.pix_fmt  # Copy pixel format from input stream to output stream
video_out.options = {'crf': '23'}  # Select low crf for high quality (the price is larger file size).
# video_out.codec_context.display_aspect_ratio = video_in.codec_context.display_aspect_ratio

i=0
for frame in src.decode(video_in):
    if(i%20==0):
        print(i, frame.dts)
    i+=1
    # img_frame = frame.to_image()
    # out_frame = av.VideoFrame.from_image(img_frame)  # Note: to_image and from_image is not required in this specific example.
    out_packet = video_out.encode(frame)  # Encode video frame
    out.mux(out_packet)  # "Mux" the encoded frame (add the encoded frame to MP4 file).

# Flush the encoder
out_packet = video_out.encode(None)
out.mux(out_packet)

# i=0
# for pack in src.demux(video_in):
#     frames = pack.decode()
#     out_packet = 0
#     for frame in frames:
#         i+=1
#         if(i%100==0):
#             frame.to_image().save(f'fram{i}.jpg')
#             # print(frame)
#             # print(av.VideoFrame.from_ndarray(frame.to_ndarray(), 'yuv420p'))
#             # out_packet = video_out.encode(frame)  # Encode video frame
#             # print(pack)
#             # print(out_packet)
#     if pack.dts == None:
#         continue
#     # pack.stream = video_out
#     # out.mux(pack)

src.close()
out.close()
