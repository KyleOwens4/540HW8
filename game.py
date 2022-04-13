import random
import copy

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    move_positions = []
    moves_made = 0
    MAX_DEPTH = 3

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        # If we're in drop phase, make sure we return a move from position
        drop_phase = (self.moves_made < 8)
        if not drop_phase:
            max_val, max_succ = self.max_value(self.board, 0)
            return self.pick_valid_move()

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        max_val, max_succ = self.max_value(self.board, 0)
        move = []
        (row, col) = (random.randint(0,4), random.randint(0,4))
        while not state[row][col] == ' ':
            (row, col) = (random.randint(0,4), random.randint(0,4))

        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, (row, col))
        self.move_positions.append((row, col))
        self.moves_made += 1
        return move

    def max_value(self, state, depth):
        value = self.heuristic_game_value(state) * -1

        if depth == self.MAX_DEPTH or value == 1 or value == -1:
            return value, state

        max_val = -10
        max_succ = []

        for succ in self.succ(state, (self.moves_made + depth) < 8, self.my_piece):
            new_val, new_succ = self.min_value(succ, depth + 1)
            if new_val > max_val:
                max_succ = succ
                max_val = new_val

        return max_val, max_succ

    def min_value(self, state, depth):
        value = self.heuristic_game_value(state)
        move_color = 'b' if self.my_piece == 'r' else 'r'

        if depth == self.MAX_DEPTH or value == 1 or value == -1:
            return value, state

        min_val = 10
        min_succ = []

        for succ in self.succ(state, (self.moves_made + depth) < 8, move_color):
            new_val, new_succ = self.max_value(succ, depth + 1)

            if new_val < min_val:
                min_succ = succ
                min_val = new_val

        return min_val, min_succ

    def pick_valid_move(self):
        moves = []
        move_pos = random.randint(0, len(self.move_positions) - 1)
        move = self.move_positions[move_pos]

        while len(moves) == 0:
            move_pos = random.randint(0, len(self.move_positions) - 1)
            move = self.move_positions[move_pos]

            # If there is room to the left of the selected position, add to the potential moves
            if move[0] > 0 and self.board[move[0] - 1][move[1]] == ' ':
                moves.append((move[0] - 1, move[1]))

            # If there is room to the right of the selected position, add to the potential moves
            if move[0] < 4 and self.board[move[0] + 1][move[1]] == ' ':
                moves.append((move[0] + 1, move[1]))

            # If there is room above the selected position, add to the potential moves
            if move[1] > 0 and self.board[move[0]][move[1] - 1] == ' ':
                moves.append((move[0], move[1] - 1))

            # If there is room below the selected position, add to the potential moves
            if move[1] < 4 and self.board[move[0]][move[1] + 1] == ' ':
                moves.append((move[0], move[1] + 1))

            # If there is room up-left of the selected position, add to the potential moves
            if move[0] > 0 and move[1] > 0 and self.board[move[0] - 1][move[1] - 1] == ' ':
                moves.append((move[0]-1, move[1]-1))

            # If there is room up-right of the selected position, add to the potential moves
            if move[0] < 4 and move[1] > 0 and self.board[move[0] + 1][move[1] - 1] == ' ':
                moves.append((move[0] + 1, move[1] - 1))

            # If there is room down-left of the selected position, add to the potential moves
            if move[0] > 0 and move[1] < 4 and self.board[move[0] - 1][move[1] + 1] == ' ':
                moves.append((move[0] - 1, move[1] + 1))

            # If there is room down-right the selected position, add to the potential moves
            if move[0] < 4 and move[1] < 4 and self.board[move[0] + 1][move[1] + 1] == ' ':
                moves.append((move[0] + 1, move[1] + 1))

        del self.move_positions[move_pos]

        selected_pos = random.randint(0, len(moves) - 1)
        self.move_positions.append(moves[selected_pos])
        return [moves[selected_pos], move]

    def succ(self, state, is_drop_phase, move_color):
        succ_states = []

        if is_drop_phase:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        state_copy = copy.deepcopy(state)
                        state_copy[row][col] = move_color
                        succ_states.append(state_copy)
        else:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == move_color:
                        self.get_swaps(state, row, col, succ_states)

        return succ_states

    def get_swaps(self, state, row, col, succ_states):

        # If there is room to the left of the selected position, add to the potential moves
        if row > 0 and state[row - 1][col] == ' ':
            state_copy = copy.deepcopy(state)
            state_copy[row - 1][col] = state[row][col]
            state_copy[row][col] = ' '
            succ_states.append(state_copy)

        # If there is room to the right of the selected position, add to the potential moves
        if row < 4 and state[row + 1][col] == ' ':
            state_copy = copy.deepcopy(state)
            state_copy[row + 1][col] = state[row][col]
            state_copy[row][col] = ' '
            succ_states.append(state_copy)

        # If there is room above the selected position, add to the potential moves
        if col > 0 and state[row][col - 1] == ' ':
            state_copy = copy.deepcopy(state)
            state_copy[row][col - 1] = state[row][col]
            state_copy[row][col] = ' '
            succ_states.append(state_copy)

        # If there is room below the selected position, add to the potential moves
        if col < 4 and state[row][col + 1] == ' ':
            state_copy = copy.deepcopy(state)
            state_copy[row][col + 1] = state[row][col]
            state_copy[row][col] = ' '
            succ_states.append(state_copy)

        # If there is room up-left of the selected position, add to the potential moves
        if row > 0 and col > 0 and state[row - 1][col - 1] == ' ':
            state_copy = copy.deepcopy(state)
            state_copy[row - 1][col - 1] = state[row][col]
            state_copy[row][col] = ' '
            succ_states.append(state_copy)

        # If there is room up-right of the selected position, add to the potential moves
        if row < 4 and col > 0 and state[row + 1][col - 1] == ' ':
            state_copy = copy.deepcopy(state)
            state_copy[row + 1][col - 1] = state[row][col]
            state_copy[row][col] = ' '
            succ_states.append(state_copy)

        # If there is room down-left of the selected position, add to the potential moves
        if row > 0 and col < 4 and state[row - 1][col + 1] == ' ':
            state_copy = copy.deepcopy(state)
            state_copy[row - 1][col + 1] = state[row][col]
            state_copy[row][col] = ' '
            succ_states.append(state_copy)

        # If there is room down-right the selected position, add to the potential moves
        if row < 4 and col < 4 and state[row + 1][col + 1] == ' ':
            state_copy = copy.deepcopy(state)
            state_copy[row + 1][col + 1] = state[row][col]
            state_copy[row][col] = ' '
            succ_states.append(state_copy)

        return succ_states

    def heuristic_game_value(self, state):
        value = self.game_value(state)

        if value == 0:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == self.my_piece:
                        if row != 0 and row != 4 and col != 0 and col != 4:
                            value += .025

                        if row == 2 and col == 2:
                            value += .025

                        value += self.get_chain_value(state, row, col)

        return value

    def get_chain_value(self, state, row, col):
        chain = 1
        # Up
        if row > 1 and state[row - 1][col] == self.my_piece:
            chain += 1

        # Down
        if row < 4 and state[row + 1][col] == self.my_piece:
            chain += 1

        # Left
        if col > 1 and state[row][col - 1] == self.my_piece:
            chain += 1

        # Right
        if col < 4 and state[row][col + 1] == self.my_piece:
            chain += 1

        # Up Left
        if row > 1 and col > 1 and state[row - 1][col - 1] == self.my_piece:
            chain += 1

        # Up Right
        if row > 1 and col < 4 and state[row - 1][col + 1] == self.my_piece:
            chain += 1

        # Down Left
        if row < 4 and col > 1 and state[row + 1][col - 1] == self.my_piece:
            chain += 1

        # Down Right
        if row < 4 and col < 4 and state[row + 1][col + 1] == self.my_piece:
            chain += 1

        return chain/100

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)
        self.moves_made += 1

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins
        for col in range(2):
            for row in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row +1][col + 1] == state[row + 2][col + 2] == state[row + 3][col + 3]:
                    return 1 if state[row][col] == self.my_piece else -1

        # check / diagonal wins
        for col in range(2):
            for row in range(3, 5):
                if state[row][col] != ' ' and state[row][col] == state[row - 1][col + 1] == state[row - 2][col + 2] == state[row - 3][col + 3]:
                    return 1 if state[row][col] == self.my_piece else -1

        # check box wins
        for col in range(4):
            for row in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row][col + 1] == state[row + 1][col] == state[row + 1][col + 1]:
                    return 1 if state[row][col] == self.my_piece else -1

        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
