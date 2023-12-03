import os
from ab.container import *

def attackMovie(title, crf):
    output_file = f'{PathType.ATTACK}{title}-CRF{crf}'
    file =  output_file
    output_file = PathType.OUT + output_file
    if(os.path.isfile(f'{output_file}.mp4')):
        print('Movie exists with crf ' + str(crf))
        return file
    # Create compressed files
    os.system(f'ffmpeg -loglevel quiet -i {PathType.OUT}{title}.mp4 -c:v libx264 -crf {crf} {output_file}.mp4')
    print('Movie attacked with crf ' + str(crf))
    return file
