
import random

def max_(a, b):
    if a == None:
        return b
    elif b == None:
        return a
    else:
        return max(a, b)

def min_(a, b):
    if a == None:
        return b
    elif b == None:
        return a
    else:
        return min(a, b)

class TicTacToeAgent(object):
    def __init__(self, problem):
        self.problem = problem
        self.keep_working = True
        self.trans_table = {}

    def max_decision(self, state):
        value = None
        actions = []
        for action, next_state in self.problem.successors(state):
            next_value = self.min_value(next_state)
            if value is None or value < next_value:
                value = next_value
                actions = [action]
            elif value == next_value:
                actions.append(action)
            if self.keep_working == False:
                break
        if actions:
            return random.choice(actions)
        else:
            return None

    def min_decision(self, state):
        value = None
        actions = []
        for action, next_state in self.problem.successors(state):
            next_value = self.max_value(next_state)
            if value is None or value > next_value:
                value = next_value
                actions = [action]
            elif value == next_value:
                actions.append(action)
            if self.keep_working == False:
                break
        if actions:
            return random.choice(actions)
        else:
            return None

    def max_value(self, state, alpha=None, beta=None):
        if state in self.trans_table:
            return self.trans_table[state]
        if self.problem.is_terminal(state):
            return self.problem.utility(state)
        value = None
        for action, next_state in self.problem.successors(state):
            value = max_(value, self.min_value(next_state, alpha, beta))
            if beta is not None and value >= beta:
                return value
            alpha = max_(alpha, value)
            if self.keep_working == False:
                break
        self.trans_table[state] = value
        return value

    def min_value(self, state, alpha=None, beta=None):
        if state in self.trans_table:
            return self.trans_table[state]
        if self.problem.is_terminal(state):
            return self.problem.utility(state)
        value = None
        for action, next_state in self.problem.successors(state):
            value = min_(value, self.max_value(next_state, alpha, beta))
            if alpha is not None and value <= alpha:
                return value
            beta = min_(beta, value)
            if self.keep_working == False:
                break
        self.trans_table[state] = value
        return value


class TicTacToeProblem(object):
    def __init__(self, init_state):
        self.init_state = init_state

    def successors(self, state):
        valid_moves = state.valid_moves()
        successors = []
        for move in valid_moves:
            result_state = state.copy()
            result_state.do_action(*move)
            successors.append((move, result_state))
        return successors

    def is_terminal(self, state):
        return state.is_finished()

    def utility(self, state):
        state.is_finished()
        if state.winner == 'X':
            return 1
        elif state.winner == 'O':
            return -1
        else:
            return 0

        