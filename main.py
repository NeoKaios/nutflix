from numpy import float32
from ab.movies import createABMovies
from ab.server import * #makeMarkedMovie, markedMovieReader
from ab.watermarks.dummy import ABMarkDummy
from ab.watermarks.onepixel import ABMarkOnePixel
from ab.watermarks.qt import ABMarkQT

def makeAndRead(title: str,mark, id: int, overwrite: bool = False):
    title += '-' + mark.getMethodName()
    title = slowmakeMarkedMovie(title, id, overwrite)
    read = markedMovieReader(title, mark)
    print(f'(Expect="{bin(id)[::-1]}"/"{id}")')
    print(f'READ ID="{bin(read)[::-1]}"/"{read}"')

def testMakeAndRead(title: str,mark, id: int, overwrite: bool = False):
    title += '-' + mark.getMethodName()
    # title = makeMarkedMovie(title, id, overwrite)
    title = makeTest(title, id, overwrite)
    read = markedMovieReader(title, mark)
    print(f'(Expect="{bin(id)[::-1]}"/"{id}")')
    print(f'READ ID="{bin(read)[::-1]}"/"{read}"')

from ab.watermarks.qt import *
import matplotlib.pyplot as plt
m = ABMarkQT();
im = np.array(plt.imread('birds.jpg'), dtype=float32)

a,b = m.createABImage(im)
print(m.readFrame(a), m.readFrame(b))

movie = 'coca'
id = 44
mark = ABMarkQT()
createABMovies(movie, mark, True)
makeAndRead(movie, mark, id, True)
