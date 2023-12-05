from ab.movies import createABMovies
from ab.server import * #makeMarkedMovie, markedMovieReader
from ab.marks import getWatermark

def makeAndRead(title: str,mark, id: int, overwrite: bool = False):
    title += '-' + mark.getMethodName()
    title = makeMarkedMovie(title, id, overwrite)
    read = markedMovieReader(title, mark)
    print(f'(Expect="{bin(id)[::-1]}"/"{id}")')
    print(f'READ ID="{bin(read)[::-1]}"/"{read}"', end='  ')
    print(f'{"SUCCESS" if read==id else "FAIL"}')

movie = 'coca'
id = 44
# mark = getWatermark('qtyuv16#8')
mark = getWatermark('blockP')
createABMovies(movie, mark, False)
makeAndRead(movie, mark, id, True)
