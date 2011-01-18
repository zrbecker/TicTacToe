from copy import *

class TicTacToeState(object):
    def __init__(self, board=None, turn='X'):
        if board:
            self.board = board
        else:
            self.board = [' ' for _ in range(3 ** 2)]
        self.turn = 'X'
        self.winner = None

    def __eq__(self, other):
        return all(self.board == other.board,
                   self.turn == other.turn)

    def __hash__(self):
        return hash((tuple(self.board), self.turn))

    def __str__(self):
        result = ''
        for index, piece in enumerate(self.board):
            result += ' ' + piece + ' '
            if  index + 1 == 3 ** 2:
                pass
            elif (index + 1) % 3 == 0:
                result += '\n---|---|---\n'
            else:
                result += '|'
        return result

    def copy(self):
        return deepcopy(self)

    def valid_moves(self):
        moves = []
        if not self.is_finished():
            for index, piece in enumerate(self.board):
                if piece == ' ':
                    row = index // 3
                    col = index % 3
                    moves.append((row, col))
        return moves

    def do_action(self, row, col):
        if self.board[row * 3 + col] == ' ' and not self.is_finished():
            self.board[row * 3 + col] = self.turn
            if self.turn == 'X':
                self.turn = 'O'
            else:
                self.turn = 'X'
            self.is_finished() # Sets winner

    def is_finished(self):
        if self.winner:
            return True
        winners = [(0, 1, 2), (0, 3, 6), (0, 4, 8), (1, 4, 7),
                   (2, 5, 8), (2, 4, 6), (3, 4, 5), (6, 7, 8)]
        for (a, b, c) in winners:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                self.winner = self.board[a]
                return True
        if ' ' not in self.board:
            return True
        return False


class TicTacToeConsole(object):
    def __init__(self):
        self.state = TicTacToeState()

    def main_loop(self):
        while not self.state.is_finished():
            print self.state
            print 'It is', self.state.turn + '\'s', 'move'
            try:
                row = int(raw_input('Row: '))
                col = int(raw_input('Col: '))
                print
            except ValueError:
                print 'Invalid entry. Try again.'
                continue
            if (row, col) in self.state.valid_moves():
                self.state.do_action(row, col)
            else:
                print 'Invalid entry. Try again.'
        print self.state
        if self.state.winner:
            print 'Congrats!', self.state.winner, 'won.'
        else:
            print "Cat's game"


if __name__ == '__main__':
    play = True
    while play:
        try:
            game = TicTacToeConsole()
            game.main_loop()
            play_input = raw_input('Play again? (y/n): ')
            if play_input == 'y':
                play = True
            else:
                play = False
        except KeyboardInterrupt:
            print
            break
