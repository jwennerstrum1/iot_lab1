import utils
from grid_world import grid_world, grid_cell
# import pdb
import numpy as np

# np.set_printoptions(threshold=np.inf, linewidth=np.inf)

# filename = 'sample_map.txt'
# # filename = 'block_left.txt'


# start = (37, 24)
# end = (37, 45)


# # filename = 'block_left.txt'
# # start = (0, 0)
# # end = (2, 3),

# world = utils.readArrayFromFile(filename)
# gw = grid_world(world, start, end)
# gw.run_a_star()


def driver():
    np.set_printoptions(threshold=np.inf, linewidth=np.inf)


    # filename = 'block_left.txt'
    # start = (37, 24)
    # end = (37, 45)

    filename = 'sample_map.txt'
    start = (0, 0)
    end = (2, 3)

    world = utils.readArrayFromFile(filename)
    gw = grid_world(world, start, end)
    gw.run_a_star()
    return gw

# if __name__ == "__main__":
    # driver()
