import sys
from ab.movies import createABMovies
from ab.server import * #makeMarkedMovie, markedMovieReader
from ab.watermarks.onepixel import ABMarkOnePixel
from ab.watermarks.blockpixel import ABMarkBlockPixel
from attack2 import attackMovie

movie = 'coca'
id = 1

if(len(sys.argv) != 3):
    print('2 args expected:')
    print('- title of movie in movies/ dir')
    print('- id to mark on the movie\n')
else:
    movie = sys.argv[1]
    id = int(sys.argv[2])


mark = ABMarkOnePixel()
createABMovies(movie, mark)
title = movie + '-' + mark.getMethodName()
title = slowmakeMarkedMovie(title, id)

listCrfMovie = attackMovie(title)
print("CRF --- Mark read successfully")
for (crf, title) in listCrfMovie:
    read = markedMovieReaderLogless(title, mark)
    val = 'YES' if read == id else '-'
    print(f'{crf}  ---   {val}')
