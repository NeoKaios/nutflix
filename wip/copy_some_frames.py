import av

src = av.open('movies/oa.mp4')

i = 0
for frame in src.decode(video=0):
    i+=1
    if(i%301==100):
        frame.to_image().save('frame-%04d.jpg' % frame.index)

src.close()
