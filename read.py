import sys
from ab.movies import createABMovies
from ab.server import * #makeMarkedMovie, markedMovieReader
from ab.marks import getWatermark

if(len(sys.argv) != 3):
    print('2 args expected:')
    print('- path of movie in out/ dir')
    print('- mark type name\n')

mark = getWatermark(sys.argv[2])
if(mark):
    read = markedMovieReader(sys.argv[1], mark)
    print("Read mark: " +str(read))
else:
    print('Coundnt find a mark for name: '+sys.argv[2])
