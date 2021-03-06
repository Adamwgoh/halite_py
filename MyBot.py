import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import logging
import percepts

myID, game_map = hlt.get_init()
hlt.send_init("MyPythonBot")

count = 0
my_tiles = 0
own_tiles = []
## Colony health inspection
## =========================
## Total_strength   Total_area_covered  Highest_production_tile

## Protectism approach
## ====================
## After colony grows to a certain size, steps with the highest productions wil
## Will be invested heavily until max, and spill out to its four corners


## Greedy approach
## ====================
## Each turn of standing still will generate an estimated distance that it can
##  travel without being too weak on the borders.


#These two are the basic functions of the bot. To determine the direction of
#    the next move for a specific square
def get_move(square):
    direction = None

    # The direction of the neighboring square if the neighbor square strength is
    # weaker and does not belongs to you
    _, direction = next(((neighbor.strength, direction)
        for direction, neighbor in enumerate(game_map.neighbors(square))
            if neighbor.owner != myID and neighbor.strength < square.strength), (None, None))

    if direction is not None:
        return Move(square, direction)
    else:
        return Move(square, STILL)

    border = any(neighor.owner != myID for neighbor in game_map.neighbors(square))
    if not border:
        return Move(square, find_nearest_enemy_direction(square))
    else:
        return Move(square, STILL)


## Copied Functions
def find_nearest_enemy_direction(square):
    logging.basicConfig(filename='test.log', level=logging.DEBUG)

    direction = NORTH #defaults to go NORTH
    max_distance = min(game_map.width, game_map.height) / 2
    for d in (NORTH, EAST, SOUTH, WEST):
        distance = 0
        current = square
        while current.owner == myID and distance < max_distance:
            distance += 1
            current = game_map.get_target(current, d)
        if distance < max_distance:
            direction = d
            max_distance = distance
            logging.debug('Unowned square details : \n')
            logging.debug('x:' + str(current.x) + ', y:' + str(current.y) + '\n')
            logging.debug('ownerID: ' + str(current.owner) + '\n')
            logging.debug('strength: ' + str(current.strength) + '\n')
            logging.debug('production: ' + str(current.production) + '\n\n')
    return direction

while True:
    game_map.get_frame()
    borders = percepts.get_border_squares(game_map, own_tiles, myID)
    count += 1
    logging.debug('Round : ' + str(count))
    own_tiles = []
    my_tiles = 0 # Spaghetti is served
    for square in game_map:
        if square.owner == myID:
            my_tiles+=1
            own_tiles.append(square)
            distance = percepts.get_distance_from_nearest_border(game_map, square, borders)
            # logging.debug('distance from nearest border: ' + str(distance))
    conquerable_tiles = percepts.get_conquerable_neighbors(game_map, myID, borders)
    logging.debug('Number of Owned tiles: ' + str(my_tiles))
    logging.debug('Number of border tiles: ' + str(len(borders)))
    logging.debug('Number of conquerable tile: ' + str(len(conquerable_tiles)) + '\n\n')

    moves = [get_move(square) for square in game_map if square.owner == myID]

    hlt.send_frame(moves)
