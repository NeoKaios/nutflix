import sys
from ab.movies import createABMovies
from ab.server import * #makeMarkedMovie, markedMovieReaderLogless
from ab.marks import getWatermark
from ab.watermarks.qtyuv import ABMarkQTyuv
from attack import attackMovie

movie = 'coca'
id = 1
crf_start = 25

if(len(sys.argv) < 4):
    print('2 args expected:')
    print('- title of movie in movies/ dir')
    print('- mark type name\n')
    print('- id to mark on the movie\n')
    print('- (optional) starting crf\n')
else:
    movie = sys.argv[1]
    id = int(sys.argv[3])
    print(f"ID = {id}")
    if (len(sys.argv) > 4):
        crf_start = int(sys.argv[4])

mark = getWatermark(sys.argv[2]) or ABMarkQTyuv()
createABMovies(movie, mark)
title = movie + '-' + mark.getMethodName()
title = makeMarkedMovie(title, id)

print("CRF --- Successful read?")
for crf in range(crf_start, 52, 2):
    attackedTitle = attackMovie(title, crf)
    read = markedMovieReaderLogless(attackedTitle, mark)
    success = read==id
    val = 'YES' if success else '-'
    print(f'{crf}  ---   {val}')
    if not success:
        print(f"Fail to read mark at crf {crf}, stopping here")
        break
