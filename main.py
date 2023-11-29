import sys
sys.path.append('./ab')
sys.path.append('./ab/watermarks/')

from ab.movies import createABMovies
from ab.watermarks.dummy import ABMarkDummy


mark = ABMarkDummy()
createABMovies('coca', mark)

