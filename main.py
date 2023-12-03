from ab.movies import createABMovies
from ab.server import * #makeMarkedMovie, markedMovieReader
from ab.marks import getWatermark

def makeAndRead(title: str,mark, id: int, overwrite: bool = False):
    title += '-' + mark.getMethodName()
    title = slowmakeMarkedMovie(title, id, overwrite)
    read = markedMovieReader(title, mark)
    print(f'(Expect="{bin(id)[::-1]}"/"{id}")')
    print(f'READ ID="{bin(read)[::-1]}"/"{read}"', end='  ')
    print(f'{"SUCCESS" if read==id else "FAIL"}')

def testMakeAndRead(title: str,mark, id: int, overwrite: bool = False):
    title += '-' + mark.getMethodName()
    # title = makeMarkedMovie(title, id, overwrite)
    title = makeTest(title, id, overwrite)
    read = markedMovieReader(title, mark)
    print(f'(Expect="{bin(id)[::-1]}"/"{id}")')
    print(f'READ ID="{bin(read)[::-1]}"/"{read}"', end='  ')
    print(f'{"SUCCESS" if read==id else "FAIL"}')

# from ab.watermarks.qt import *
# import matplotlib.pyplot as plt
# m = ABMarkQTyuv();
# im = np.array(plt.imread('birds.jpg'), dtype=float32)

# a,b = m.createABImage(im)
# print(m.readFrame(a), m.readFrame(b))

movie = 'coca'
id = 44
mark = getWatermark('qtyuv16#8')
createABMovies(movie, mark, False)
makeAndRead(movie, mark, id, False)
