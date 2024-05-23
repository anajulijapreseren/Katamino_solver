import copy
from pieces_and_games import *

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
            # Generate rotations and mirror once per unique rotation found
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
        coords = [(x, y) for y, row in enumerate(config) for x, val in enumerate(row) if val == 'X']
        return self.normalize_coords(coords)

    def normalize_coords(self, coords):
        """Normalize coordinates to ensure the piece is positioned at the origin and sorted."""
        min_x = min(x for x, y in coords)
        min_y = min(y for x, y in coords)
        shifted = [(x - min_x, y - min_y) for x, y in coords]
        normalized = sorted(shifted)
        return normalized

    def rotate(self, coords):
        """Rotate coordinates 90 degrees clockwise."""
        return [(y, -x) for x, y in coords]

    def mirror(self, coords):
        """Mirror coordinates horizontally."""
        return [(-x, y) for x, y in coords]

    def can_add_to_board(self, board, coords, offset):
        """Check if the piece can be placed on the board."""
        ox, oy = offset
        for x, y in coords:
            if not (0 <= x + ox < len(board[0]) and 0 <= y + oy < len(board)):
                return False
            if board[y + oy][x + ox] != -1:
                return False
        return True

    def add_to_board(self, board, coords, offset):
        """Place a piece on the board."""
        ox, oy = offset
        for x, y in coords:
            board[y + oy][x + ox] = self.name

    def remove_from_board(self, board, coords, offset):
        """Remove a piece from the board."""
        ox, oy = offset
        for x, y in coords:
            board[y + oy][x + ox] = -1

    def offsets_to_fill_pos(self, pos):
        """Returns offsets in which this piece would fill the specified pos."""
        result = []
        for coords in self.orientations:
            for x, y in coords:
                ox = pos[0] - x
                oy = pos[1] - y
                result.append((ox, oy))
        return result



def find_available_pos_in_board(board):
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == -1:
                return j, i
    return None

def solve(pieces, board, depth):
    if len(pieces) == 0:
        return board

    pos = find_available_pos_in_board(board)
    if not pos:
        #print('No available position on board!')
        return
    #print_board(board, depth)
    #print('  '*depth + 'Trying to fill position %d,%d' % pos)

    for piece_num, piece in enumerate(pieces):
        new_pieces = pieces[:piece_num] + pieces[piece_num+1:]
        for orientation in piece.orientations:
            for offset in piece.offsets_to_fill_pos(pos):
                if piece.can_add_to_board(board, orientation, offset):
                    piece.add_to_board(board, orientation, offset)
                    solution = solve(new_pieces, board, depth+1)
                    if solution:
                        return solution
                    piece.remove_from_board(board, orientation, offset)
    #print('  '*depth + 'No solution, backing up.')
    return None

# def print_board(board, indent):
#     for row in board:
#         print('  '*indent + ' '.join(str(x) if x != -1 else '.' for x in row))
#     print()

def print_board(board, indent):
    print(' '+ '_ '*len(board[0]))
    for i in range(len(board)-1):
        print('|', end='')
        for j in range(len(board[0])-1):
            this = board[i][j]
            right = board[i][j+1]
            #print(board[i][j], end='')            
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

# Usage example with defined pieces
# Define your pieces and call solve(pieces) accordingly
PIECES_DEF1 = {
    'T1': [
        ['XX',
         'X ',
         'X ']
    ],
    'I2':[['X','X']]
    # 'T2': [
    #     [' X ',
    #      'XXX']
    # ],
    # 'L4': [
    #     [' X',
    #      'XX']
    # ],
    # 'Z5': [
    #     ['XX ',
    #      ' XX']
    # ],
    # 'I3': [
    #     ['X']
    # ]
}

PIECES_DEF={
    
    'L5':[
        ['XX',
         'X ',
         'X ',
         'X ' ]],
    'F5':[ 
        ['X ',
         'XX',
         'X ',
         'X ' ]],
    'T5':[ 
        [' X ',
         ' X ',
         'XXX' ]],
    'P5':[ 
        ['XX',
         'XX',
         'X ']],
    'M5':[ 
        ['XX ',
         ' XX',
         '  X']],
    'Z5':[ 
        ['XX ',
         ' X ',
         ' XX']]
  
}



# if __name__ == '__main__':
#     # Example usage:
#     board = [[-1] * 3 for _ in range(2)]  # Those 2 numbers are width and height of the board
#     pieces = [Piece(v, k) for k, v in PIECES_DEF1.items()]
#     solution = solve(pieces,board,0)
#     if solution:
#         print('=== SOLVED! ===')
#         print_board(solution,0)
#     else:
#         print('No Solution!')

if __name__ == '__main__':
    # Example usage
    while True:
        game_id = input('Which game do you want to solve? (Enter a letter a-d followed by a number 4-11)\n') # For example: a5
        if game_id[0] not in games.keys() or game_id[1:] not in ['4', '5', '6', '7', '8', '9', '10', '11']:
            print("Invalid entry!")
            continue
        else:
            break
    game_letter = game_id[0]
    game_size = int(game_id[1:])
    board = make_board(game_size)
    selected_pieces = {k: ALL_PIECES[k] for k in games[game_letter][:game_size]}
    pieces = [Piece(v, k) for k, v in selected_pieces.items()]
    solution = solve(pieces,board,0)
    if solution:
        print('=== SOLVED! ===')
        print_board(solution,0)
    else:
        print('No Solution!')
