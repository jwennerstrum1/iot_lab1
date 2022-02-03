from path_follow import get_turn_idx, direction
import pdb


turn_dir = ["turn_left", "turn_right"]

def test_get_turn_idx1():
    # current node is in front we shouldn't change direction
    idx = get_turn_idx((0,0), (0,1), direction.NORTH)
    assert idx is None

    idx = get_turn_idx((0,0), (1,0), direction.WEST)
    assert idx is None


def test_get_turn_idx2():
    idx = get_turn_idx((0, 0), (0,1), direction.WEST)
    assert turn_dir[idx] == "turn_right"

    idx = get_turn_idx((0,0), (0,1), direction.EAST)
    assert turn_dir[idx] == "turn_left"
    
    idx = get_turn_idx((0,0), (0,-1), direction.EAST)
    assert turn_dir[idx] == "turn_right"
    
    idx = get_turn_idx((0,0), (1,0), direction.SOUTH)
    assert turn_dir[idx] == "turn_left"

    idx = get_turn_idx((0,0), (-1,0), direction.SOUTH)
    assert turn_dir[idx] == "turn_right"

    idx = get_turn_idx((0,0), (-1,0), direction.NORTH)
    assert turn_dir[idx] == "turn_left"
