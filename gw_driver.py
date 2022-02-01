import utils
import astart
# import pdb
import numpy as np

np.set_printoptions(threshold=np.inf, linewidth=np.inf)

# filename = 'test_map.txt'


filename = 'block_left.txt'
start = (37, 24)
end = (37, 45)


# filename = 'block_left.txt'
# start = (0, 0)
# end = (2, 3)



world = utils.readArrayFromFile(filename)
gw = astart.grid_world(world, start, end)
gw.run_a_start()

