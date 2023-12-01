from ab.movies import createABMovies
from ab.server import * #makeMarkedMovie, markedMovieReader
from ab.watermarks.dummy import ABMarkDummy
from ab.watermarks.onepixel import ABMarkOnePixel
from ab.watermarks.blockpixel import ABMarkBlockPixel

def makeAndRead(title: str,mark, id: int, overwrite: bool = False):
    title += '-' + mark.getMethodName()
    # title = makeMarkedMovie(title, id, overwrite)
    title = slowmakeMarkedMovie(title, id, overwrite)
    read = markedMovieReader(title, mark)
    print(f'(Expect="{bin(id)[::-1]}"/"{id}")')
    print(f'READ ID="{bin(read)[::-1]}"/"{read}"')

movie = 'oa'
mark = ABMarkBlockPixel()
createABMovies(movie, mark)
# title = makeMarkedMovie(movie + '-' + mark.getMethodName(), 1, True)
makeAndRead(movie, mark, 2736, False)




# makeAndRead(movie, mark, 2)
# makeAndRead(movie, mark, 4)
# makeAndRead(movie, mark, 8)
