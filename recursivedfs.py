from pieces_and_games import *
import time
import matplotlib.pyplot as plt
from tqdm import tqdm
import random

class Piece:
    """A class to handle piece operations like rotation and placement."""
    def __init__(self, definition, name):
        self.name = name
        self.orientations = self.generate_orientations(definition)

    def generate_orientations(self, definition):
        """Generate all unique orientations of the piece."""
        orientations = []
        unique_orientations = set()

        for config in definition:
            piece = self.normalize(config)

            # Generate rotations
            for _ in range(4):
                normalized_piece = self.normalize_coords(piece)
                piece_str = str(normalized_piece)
                if piece_str not in unique_orientations:
                    unique_orientations.add(piece_str)
                    orientations.append(normalized_piece)
                piece = self.rotate(piece)
            
            # Generate mirrored orientations
            piece = self.mirror(piece)
            for _ in range(4):
                normalized_piece = self.normalize_coords(piece)
                piece_str = str(normalized_piece)
                if piece_str not in unique_orientations:
                    unique_orientations.add(piece_str)
                    orientations.append(normalized_piece)
                piece = self.rotate(piece)

        return orientations

    def normalize(self, config):
        """Normalize piece coordinates."""
        coords = [(x, y) for y in range(len(config)) for x in range(len(config[0])) if config[y][x] == 'X']
        return self.normalize_coords(coords)

    def normalize_coords(self, coords):
        """Normalize coordinates to ensure the piece is positioned at the origin and sorted."""
        min_x = min(x for x, _ in coords)
        min_y = min(y for _, y in coords)
        shifted = [(x - min_x, y - min_y) for x, y in coords]
        normalized = sorted(shifted)
        return normalized

    def rotate(self, coords):
        """Rotate coordinates 90 degrees clockwise."""
        return [(y, -x) for x, y in coords]

    def mirror(self, coords):
        """Mirror coordinates horizontally."""
        return [(-x, y) for x, y in coords]

    def can_add_piece(self, board, coords, offset):
        """Check if the piece can be placed on the board."""
        ox, oy = offset
        for x, y in coords:
            if not (0 <= x + ox < len(board[0]) and 0 <= y + oy < len(board)):
                return False
            if board[y + oy][x + ox] != -1:
                return False
        return True

    def add_piece(self, board, coords, offset):
        """Place a piece on the board."""
        ox, oy = offset
        for x, y in coords:
            board[y + oy][x + ox] = self.name

    def remove_piece(self, board, coords, offset):
        """Remove a piece from the board."""
        ox, oy = offset
        for x, y in coords:
            board[y + oy][x + ox] = -1

    def get_offsets(self, pos, coords):
        """Get all possible offsets in which the piece fills the specified position."""
        result = []
        # for coords in self.orientations:
        for x, y in coords:
            ox = pos[0] - x
            oy = pos[1] - y
            if (ox,oy) not in result: # Keep only unique offsets
                result.append((ox, oy))
        return result



def find_empty_position(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == -1:
                return j, i
    return None

def solve(pieces, board):
    if len(pieces) == 0:
        return board

    pos = find_empty_position(board)
    if not pos:
        # print('No empty position on board!')
        return
    print_board(board)
    print('Trying to fill position %d,%d' % pos)
    # time.sleep(2)

    for piece in pieces:
        available_pieces = pieces.copy()
        available_pieces.remove(piece)
        for orientation in piece.orientations:
            for offset in piece.get_offsets(pos, orientation):
                if piece.can_add_piece(board, orientation, offset):
                    piece.add_piece(board, orientation, offset)
                    solution = solve(available_pieces, board)
                    if solution:
                        return solution
                    piece.remove_piece(board, orientation, offset)
    print('No solution, backtracking.')
    return None


def print_board(board):
    print(' '+ '_ '*len(board[0]))
    for i in range(len(board)-1):
        print('|', end='')
        for j in range(len(board[0])-1):
            this = board[i][j]
            right = board[i][j+1]          
            if i <= len(board)-2:
                down = board[i+1][j]
                if this != down:
                    print('_', end='')
                else:
                    print(' ', end='')
            if this != right:
                print('|', end='')
            else:
                print(' ', end='')

        if i <= len(board)-2:
            down = board[i+1][-1]
            if board[i][-1] != down:
                print('_|')
            else:
                print(' |')
    print('|', end='')
    for j in range(len(board[0])-1):
        this = board[-1][j]
        right = board[-1][j+1]
        if this != right:
            print('_|', end='')
        else:
            print('_ ', end='')
    print('_|')
    print()


depth = [4,5,6,7,8,9,10,11,12]
time_a = [0, 0.009, 0.120, 1.582, 2.303, 14.933, 16.879, 32.565, 75.112]
time_b = [0, 0.030, 0.138, 0.343, 7.684, 2.724, 9.760, 8.123, 6.713]
time_c = [0, 0.048, 0.401, 2.392, 0.206, 4.392, 3.331, 0.515, 21.069]
time_d = [0, 0.016, 0.056, 0.162, 2.006, 2.491, 19.538, 100.916, 46.493]

time_ = [sum(y) for y in zip([sum(x) for x in zip(time_a, time_b)], [sum(x) for x in zip(time_c, time_d)])]
time_p = [0.0035, 0.014, 0.068, 0.631, 1.249, 7.549, 22.161, 36.682, 115.55]

# plt.plot(depth, time_p)
# plt.xlabel('depth')
# plt.ylabel('time[s]')
# plt.show()



def permutation(lst):
    if len(lst) == 0:
        return []
    if len(lst) == 1:
        return [lst]
    
    one_permutation = []

    for i in range(len(lst)):
       m = lst[i]
       remaining = lst[:i] + lst[i+1:]
       for p in permutation(remaining):
           one_permutation.append([m] + p)
    return one_permutation



if __name__ == '__main__':

    # FINDING SOLUTIONS
    while True:
        game_id = input('Which game do you want to solve? (Enter a letter a-d followed by a number 4-12)\n') # For example: a5
        if game_id[0] not in games.keys() or game_id[1:] not in ['4', '5', '6', '7', '8', '9', '10', '11', '12']:
            print("Invalid entry!")
            continue
        else:
            break
    start = time.time()
    game_letter = game_id[0]
    game_size = int(game_id[1:])
    board = make_board(game_size)
    selected_pieces = {k: ALL_PIECES[k] for k in games[game_letter][:game_size]}
    pieces = [Piece(v, k) for k, v in selected_pieces.items()]
    solution = solve(pieces,board)

    #######################################################################################
    # TIME COMPLEXITY
    # game_id = 'a11'
    
    # game_letter = game_id[0]
    # game_size = int(game_id[1:])
    # board = make_board(game_size)
    # selected_pieces = games[game_letter][:game_size]
    # p = selected_pieces
    # # permutations = permutation(selected_pieces)
    # # n = len(permutations)
    # # random_permutations = [random.randrange(n) for _ in range(10)]
    # sum_time = 0
    # for i in tqdm(range(10)):
    #     random.shuffle(p)
    #     board = make_board(game_size)
    #     permuted_pieces = {k: ALL_PIECES[k] for k in p}
    #     pieces = [Piece(v, k) for k, v in permuted_pieces.items()]
    #     start = time.time()
    #     solution = solve(pieces,board)    
    #     sum_time += time.time()-start

    ##################################################################################################

    if solution:
        print('=== SOLUTION! ===')
        print_board(solution)
        # print('Time: ' + str(sum_time/10))
        print('Time: ' + str(time.time()-start))
    else:
        print('No Solution!')
