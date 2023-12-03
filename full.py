import sys
from ab.movies import createABMovies
from ab.server import * #makeMarkedMovie, markedMovieReader
from ab.marks import getWatermark
from ab.watermarks.qtyuv import ABMarkQTyuv
from attack2 import attackMovie

movie = 'coca'
id = 1

if(len(sys.argv) != 4):
    print('2 args expected:')
    print('- title of movie in movies/ dir')
    print('- mark type name\n')
    print('- id to mark on the movie\n')
else:
    movie = sys.argv[1]
    id = int(sys.argv[3])


mark = getWatermark(sys.argv[2]) or ABMarkQTyuv()
createABMovies(movie, mark)
title = movie + '-' + mark.getMethodName()
title = slowmakeMarkedMovie(title, id)

print("CRF --- Successful read?")
for crf in range(25, 52, 2):
    attackedTitle = attackMovie(title, crf)
    read = markedMovieReaderLogless(attackedTitle, mark)
    val = 'YES' if read == id else '-'
    print(f'{crf}  ---   {val}')
