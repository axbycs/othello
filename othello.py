# Global variables
BOARD_SIZE = 8
PLAYER_A = "○"
PLAYER_B = "●"
VALID_PLAY_MARKER = "√"
PIECES = []
VALID_PLAYS = []


# Classes
class Piece:
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char

    def is_placed_here(self, x, y):
        return self.x == x and self.y == y

    def to_coordinates(self):
        return [self.x, self.y]

    def change_piece(self, char):
        self.char = char

    def __str__(self):
        return self.char


class ValidPlay:
    def __init__(self, x, y, coordinates):
        self.x = x
        self.y = y
        self.coordinates = coordinates

    def is_placed_here(self, x, y):
        return self.x == x and self.y == y


# Functions
def get_char_to_coor(x, y):
    found = " "
    for v in VALID_PLAYS:
        if v.is_placed_here(x, y):
            found = VALID_PLAY_MARKER
    if found == " ":
        for p in PIECES:
            if p.is_placed_here(x, y):
                found = p.char
    return found


def print_board():
    print("    " + "   ".join(list(map(str, range(1, BOARD_SIZE + 1)))) + "  ◄ X")
    print("  ┌" + "───┬" * (BOARD_SIZE - 1) + "───┐")
    for y in range(1, BOARD_SIZE + 1):
        if y != 1:
            print("  ├" + "───┼" * (BOARD_SIZE - 1) + "───┤")
        x_line = str(y) + " │"
        for x in range(1, BOARD_SIZE + 1):
            x_line += " " + get_char_to_coor(x, y) + " │"
        print(x_line)
    print("  └" + "───┴" * (BOARD_SIZE - 1) + "───┘")
    print("▲")
    print("Y")
    print("Valid plays are marked with '" + VALID_PLAY_MARKER + "'.")


def user_input():
    next_char_x = input("Insert x coordinate: ")
    while type(next_char_x) is not int:
        try:
            next_char_x = int(next_char_x)
            if next_char_x > BOARD_SIZE:
                raise Exception
        except:
            print("Insert a valid coordinate!")
            next_char_x = input("Insert x coordinate: ")
    next_char_y = input("Insert y coordinate: ")
    while type(next_char_y) is not int:
        try:
            next_char_y = int(next_char_y)
            if next_char_y > BOARD_SIZE:
                raise Exception
        except:
            print("Insert a valid coordinate!")
            next_char_y = input("Insert y coordinate: ")
    return next_char_x, next_char_y


def valid_plays(turn):
    turn_pieces = []
    not_turn_pieces = []
    blank_spaces = []
    for piece in PIECES:
        if piece.char == turn:
            turn_pieces.append(piece.to_coordinates())
        else:
            not_turn_pieces.append(piece.to_coordinates())
    for x in range(1, BOARD_SIZE + 1):
        for y in range(1, BOARD_SIZE + 1):
            if [x, y] not in turn_pieces and [x, y] not in not_turn_pieces:
                blank_spaces.append([x, y])
    for piece in turn_pieces:
        for space in blank_spaces:
            is_edible, coordinates = can_eat(
                piece[0], piece[1], space[0], space[1], not_turn_pieces
            )
            if is_edible:
                VALID_PLAYS.append(ValidPlay(space[0], space[1], coordinates))


def can_eat(x1, y1, x2, y2, not_turn_pieces):
    is_edible = True
    coordinates = []
    if x1 == x2 or y1 == y2 or abs(y2 - y1) == abs(x2 - x1):
        coordinates = generate_coordinates(x1, x2, y1, y2)
    if len(coordinates) > 0:
        for coor in coordinates:
            if coor not in not_turn_pieces:
                is_edible = False
    else:
        is_edible = False
    return is_edible, coordinates


def generate_coordinates(x1, x2, y1, y2):
    coordinates = []
    x_step = 0
    y_step = 0
    diff = abs(x1 - x2)
    if diff == 0:
        diff = abs(y1 - y2)
    if x1 - x2 > 0:
        x_step = -1
    elif x1 - x2 < 0:
        x_step = 1
    if y1 - y2 > 0:
        y_step = -1
    elif y1 - y2 < 0:
        y_step = 1
    x_aux = x1
    y_aux = y1
    for i in range(diff - 1):
        x_aux += x_step
        y_aux += y_step
        coordinates.append([x_aux, y_aux])
    return coordinates


def eat_pieces(x, y, turn):
    global PIECES
    coordinates_of_pieces_to_change = []
    for v in VALID_PLAYS:
        if v.is_placed_here(x, y):
            coordinates_of_pieces_to_change += v.coordinates
    for p in PIECES:
        for c in coordinates_of_pieces_to_change:
            if p.x == c[0] and p.y == c[1]:
                p.change_piece(turn)
    PIECES.append(Piece(x, y, turn))


def end_game(made_a_play_last_turn):
    if len(VALID_PLAYS) == 0 and not made_a_play_last_turn:
        a_pieces = []
        b_pieces = []
        for piece in PIECES:
            if piece.char == PLAYER_A:
                a_pieces.append(piece)
            else:
                b_pieces.append(piece)
        print_board()
        print("Player " + PLAYER_A + " has " + str(len(a_pieces)) + ".")
        print("Player " + PLAYER_B + " has " + str(len(b_pieces)) + ".")
        if len(a_pieces) > len(b_pieces):
            print("Player " + PLAYER_A + " wins!")
        else:
            print("Player " + PLAYER_B + " wins!")
        return True
    else:
        return False


def game_engine():
    # Initial state
    global VALID_PLAYS
    global PIECES
    PIECES.append(Piece(4, 4, PLAYER_A))
    PIECES.append(Piece(5, 5, PLAYER_A))
    PIECES.append(Piece(4, 5, PLAYER_B))
    PIECES.append(Piece(5, 4, PLAYER_B))
    turn = PLAYER_B
    made_a_play_last_turn = True
    valid_plays(turn)
    # Bucle engine
    while not end_game(made_a_play_last_turn):
        if len(VALID_PLAYS) > 0:
            print_board()
            print("Turn: " + turn)
            x, y = user_input()
            found = False
            for v in VALID_PLAYS:
                if v.is_placed_here(x, y):
                    found = True
            if found:
                eat_pieces(x, y, turn)
                VALID_PLAYS = []
                made_a_play_last_turn = True
                if turn == PLAYER_A:
                    turn = PLAYER_B
                else:
                    turn = PLAYER_A
            else:
                print("That is not a valid play! Try again.")
        else:
            made_a_play_last_turn = False
            if turn == PLAYER_A:
                turn = PLAYER_B
            else:
                turn = PLAYER_A
        valid_plays(turn)
    print("... End of the game ...")


def main():
    game_engine()


if __name__ == "__main__":
    main()
