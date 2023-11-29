import sys
sys.path.append('./ab')
sys.path.append('./ab/watermarks/')

from ab.movies import createABMovies
from ab.server import makeMarkedMovie
from ab.watermarks.dummy import ABMarkDummy


mark = ABMarkDummy()
# createABMovies('coca', mark)
makeMarkedMovie('coca-' + mark.getMethodName(), 10)

