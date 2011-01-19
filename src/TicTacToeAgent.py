
import random

class TicTacToeAgent(object):
    def __init__(self, problem):
        self.problem = problem
        self.keep_working = True

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

    def max_value(self, state):
        if self.problem.is_terminal(state):
            return self.problem.utility(state)
        value = None
        for action, next_state in self.problem.successors(state):
            if value is not None:
                value = max(value, self.min_value(next_state))
            else:
                value = self.min_value(next_state)
            if self.keep_working == False:
                break
        return value

    def min_value(self, state):
        if self.problem.is_terminal(state):
            return self.problem.utility(state)
        value = None
        for action, next_state in self.problem.successors(state):
            if value is not None:
                value = min(value, self.max_value(next_state))
            else:
                value = self.max_value(next_state)
            if self.keep_working == False:
                break
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

        