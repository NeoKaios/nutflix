import os
from ab.container import *

def attackMovie(title):
    files = []
    for i in range(23, 52, 2):
        output_file = f'{PathType.ATTACK}{title}-CRF{i}'
        files += [(i, output_file)]
        output_file = PathType.OUT + output_file
        if(os.path.isfile(f'{output_file}.mp4')):
            print('Movie exists with crf ' + str(i))
            continue
        # Create compressed files
        os.system(f'ffmpeg -loglevel quiet -i {PathType.OUT}{title}.mp4 -c:v libx264 -crf {i} {output_file}.mp4')
        print('Movie attacked with crf ' + str(i))
    return files
