import av

s = av.open('movies/coca.mp4')
o = av.open('out/vid.mp4')
show_all=False

c = s.streams.video[0].options
cc = o.streams.video[0].options
for d in dir(c):
    if(d[0]=='_'):
        continue
    ac = getattr(c, d)
    acc = getattr(cc, d)
    if(ac!=acc or show_all):
        print(d,ac,acc)

s.close()
o.close()
