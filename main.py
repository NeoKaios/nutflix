from ab.movies import createABMovies
from ab.server import makeMarkedMovie, markedMovieReader
from ab.watermarks.dummy import ABMarkDummy
from ab.watermarks.onepixel import ABMarkOnePixel


mark = ABMarkOnePixel()
# createABMovies('coca', mark)
title = makeMarkedMovie('coca-' + mark.getMethodName(), 12)

read = markedMovieReader(title, mark)
print(f'READ ID="{read}"')

