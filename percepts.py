import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import logging

## Percepts needed
## Ability to observe the whole of map and plan/react accordingly


border = []
logging.basicConfig(filename='test.log', level=logging.DEBUG)
# Returns a list of tiles owned by you at the border.
def get_border_squares(GameMap, own_tiles, ownerID):
    border = []
    for square in own_tiles:
        #logging.debug("square ownerID: " + str(square.owner))
        for neighbor in GameMap.neighbors(square):
            if neighbor.owner != ownerID and square.owner == ownerID:
                border.append(square)

    assert len(border) < GameMap.width * GameMap.height
    return border
#    logging.debug("border size at this point : " + str(len(border)))

# Returns the Manhattan-distance from the specified square to the nearest border
def get_distance_from_nearest_border(GameMap, square, b_squares):
    nearest = GameMap.width * GameMap.height
    # logging.debug("border size : " + str(len(b_squares)))
    for b_square in b_squares:
        distance = GameMap.get_distance(b_square, square)
        # logging.debug("distance : " + str(distance))
        if distance < nearest:
            nearest = distance

    return nearest

# Returns an array of squares that are weak enough to be conquered by the user.
# This includes NPC as well as player tiles.
# Return an array of true/false to tell if each border has conquerable tiles
def get_conquerable_neighbors(GameMap, OwnerID, borders):
    decisions = []
    neighbors = []
    for b_square in borders:
        for neighbor in GameMap.neighbors(b_square):
            if (neighbor.strength < b_square.strength and neighbor.owner != OwnerID):
                neighbors.append(neighbor)

    return neighbors
# A U-trap is a conquerable tile that is surrounded by stronger adjacent tiles
# That means when the tile is taken, the adjacent tile can effectively reclaim
# it and claim power. This function, however, only checks on the conquerable
# tiles' adjacents to see if it's a U-trap
#def check_u_trap(square):
