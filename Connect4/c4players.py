import random
import copy

PLAYER1 = 1
PLAYER2 = 2
EMPTY = -1
inf = float('inf')

class ConnectFourPlayer:

    def get_move(self):
        # Must return a value between 0 and 6 (inclusive), where 0 is the left-most column and 6 is the right-most column.
        raise NotImplementedError('Must be implemented by subclass')

    def is_automated(self):
        # AI players should return True, human players should return False
        return True


class ConnectFourHumanPlayer(ConnectFourPlayer):
    def __init__(self, model):
        self.model = model

    def is_automated(self):
        return False

    def get_move(self):
        valid_input = False
        valid_columns = self.model.get_valid_moves()

        while not valid_input:
            try:
                column = int(input('Enter column (1-7): '))
                if column < 1 or column > 7:
                    raise ValueError()
                else:
                    valid_input = True

                if valid_columns[column-1]:
                    return column-1
                else:
                    print('That column is full. Pick again.')
                    valid_input = False
            except ValueError:
                print('Invalid input.')

        # Should not get here
        return -1


class ConnectFourRandomPlayer(ConnectFourPlayer):
    def __init__(self, model):
        self.model = model

    def get_move(self):
        moves = self.model.get_valid_moves()
        #print(str(moves))
        m = random.randrange(7)
        while not moves[m]:
            m = random.randrange(7)
        return m

class ConnectFourAIPlayer(ConnectFourPlayer):
    def __init__(self, model, cutoff):
        self.model = model
        self.cutoff = cutoff
        self.col = 0
        self.turn = model.get_turn()

    # Just drops stuff from left to right
    def dumb_get_move(self):
        moves = self.model.get_valid_moves()
        m = ((self.col) % 7)
        self.col += 1
        while not moves[m]:
            m = ((self.col) % 7)
            self.col += 1
        return m


    def get_move(self):
        if self.model.get_grid()[3][5] == EMPTY:
            return 3
        return self.alpha_beta_search(self.model.get_grid(), self.cutoff)

    # action is an integer 0-6
    def result(self, state, action):
        newstate = copy.deepcopy(state)
        #print(newstate)
        turn = self._get_turn(state)
        row = 5
        while newstate[action][row] != EMPTY:
            row -= 1
        newstate[action][row] = turn
        #print(newstate)
        return newstate

    def actions(self, state):
        valid_actions = []
        for x in range(7):
            if state[x][0] == EMPTY:
                valid_actions.append(x)
        #print(valid_actions)
        return valid_actions

    def terminal_test(self, state):
        win = self.get_winner(state)

        if win > 0 or self.check_for_draw(state):
            return True
            
        return False

    def utility(self, state):
        if not self.terminal_test(state):
            return self.eval(state)
        if self.get_winner(state) == self.turn:
            return 1000
        elif self.get_winner(state) is not EMPTY:
            return -1000
        if self.check_for_draw(state):
            return 0
        return 0 # Should not happen

    def eval(self, state):
        one_streaks = 0
        two_streaks = 0
        three_streaks = 0
        one_streaks_other = 0
        two_streaks_other = 0
        three_streaks_other = 0


        count = self.__check_horizontal_streaks(state)
        one_streaks += count[0]
        two_streaks += count[1]
        three_streaks += count[2]
        one_streaks_other += count[3]
        two_streaks_other += count[4]
        three_streaks_other += count[5]

        count = self.__check_vertical_streaks(state)
        one_streaks += count[0]
        two_streaks += count[1]
        three_streaks += count[2]
        one_streaks_other += count[3]
        two_streaks_other += count[4]
        three_streaks_other += count[5]

        count = self.__check_neg_diagonal_streaks(state)
        one_streaks += count[0]
        two_streaks += count[1]
        three_streaks += count[2]
        one_streaks_other += count[3]
        two_streaks_other += count[4]
        three_streaks_other += count[5]

        count = self.__check_pos_diagonal_streaks(state)
        one_streaks += count[0]
        two_streaks += count[1]
        three_streaks += count[2]
        one_streaks_other += count[3]
        two_streaks_other += count[4]
        three_streaks_other += count[5]

        score = (100*three_streaks + 10*two_streaks + 1*one_streaks) - (100*three_streaks_other + 10*two_streaks_other + 1*one_streaks_other)
        return score


    def __check_horizontal_streaks(self, state):
        one_streaks = 0
        two_streaks = 0
        three_streaks = 0
        one_streaks_other = 0
        two_streaks_other = 0
        three_streaks_other = 0
        for row in range(6):
            for col in range(5):
                if state[col][row] == self.turn:
                    one_streaks += 1
                    if state[col][row] == state[col+1][row]:
                        two_streaks += 1
                        one_streaks -= 1
                        if state[col][row] == state[col + 2][row]:
                            three_streaks += 1
                            two_streaks -= 1    # If the streak was a three-streak
                elif state[col][row] != EMPTY:
                    one_streaks_other += 1
                    if state[col][row] == state[col+1][row]:
                        two_streaks_other += 1
                        one_streaks_other -= 1
                        if state[col][row] == state[col + 2][row]:
                            three_streaks_other += 1
                            two_streaks_other -= 1
        return [one_streaks, two_streaks, three_streaks, one_streaks_other, two_streaks_other, three_streaks_other]

    def __check_vertical_streaks(self, state):
        one_streaks = 0
        two_streaks = 0
        three_streaks = 0
        one_streaks_other = 0
        two_streaks_other = 0
        three_streaks_other = 0
        for col in range(7):
            for row in range(3):
                if state[col][row] == self.turn:
                    one_streaks += 1
                    if state[col][row] == state[col][row + 1]:
                        two_streaks += 1
                        one_streaks -= 1
                        if state[col][row] == state[col][row + 2]:
                            three_streaks += 1
                            two_streaks -= 1
                elif state[col][row] != EMPTY:
                    one_streaks_other += 1
                    if state[col][row] == state[col][row + 1]:
                        two_streaks_other += 1
                        one_streaks_other -= 1
                        if state[col][row] == state[col][row + 2]:
                            three_streaks_other += 1
                            two_streaks_other -= 1
        return [one_streaks, two_streaks, three_streaks, one_streaks_other, two_streaks_other, three_streaks_other]

    def __check_pos_diagonal_streaks(self, state):
        one_streaks = 0
        two_streaks = 0
        three_streaks = 0
        one_streaks_other = 0
        two_streaks_other = 0
        three_streaks_other = 0
        for col in range(3, 7):
            for row in range(3):
                if state[col][row] == self.turn:
                    one_streaks += 1
                    if state[col][row] == state[col - 1][row + 1]:
                        two_streaks += 1
                        one_streaks -= 1
                        if state[col][row] == state[col - 2][row + 2]:
                            three_streaks += 1
                            two_streaks -= 1
                elif state[col][row] != EMPTY:
                    one_streaks_other += 1
                    if state[col][row] == state[col - 1][row + 1]:
                        two_streaks_other += 1
                        one_streaks_other -= 1
                        if state[col][row] == state[col - 2][row + 2]:
                            three_streaks_other += 1
                            two_streaks_other -= 1
        return [one_streaks, two_streaks, three_streaks, one_streaks_other, two_streaks_other, three_streaks_other]

    def __check_neg_diagonal_streaks(self, state):
        one_streaks = 0
        two_streaks = 0
        three_streaks = 0
        one_streaks_other = 0
        two_streaks_other = 0
        three_streaks_other = 0
        for col in range(4):
            for row in range(3):
                if state[col][row] == self.turn:
                    one_streaks += 1
                    if state[col][row] == state[col + 1][row + 1]:
                        two_streaks += 1
                        one_streaks -= 1
                        if state[col][row] == state[col + 2][row + 2]:
                            three_streaks += 1
                            two_streaks -= 1
                elif state[col][row] != EMPTY:
                    one_streaks_other += 1
                    if state[col][row] == state[col + 1][row + 1]:
                        two_streaks_other += 1
                        one_streaks_other -= 1
                        if state[col][row] == state[col + 2][row + 2]:
                            three_streaks_other += 1
                            two_streaks_other -= 1
        return [one_streaks, two_streaks, three_streaks, one_streaks_other, two_streaks_other, three_streaks_other]



        

    def get_winner(self, state):
        win = self.__check_horizontal_win(state)
        if win < 0:
            win = self.__check_vertical_win(state)
        if win < 0:
            win = self.__check_neg_diagonal_win(state)
        if win < 0:
            win = self.__check_pos_diagonal_win(state)

        return win

    def check_for_draw(self, state):
        for i in range(7):
            for j in range(6):
                if state[i][j] == EMPTY:
                    return False
        return True

    def alpha_beta_search(self, state, cutoff):
        alpha = -inf
        beta = inf
        best_action = None
        for a in self.actions(state):
            v = self.max_value(self.result(state, a), alpha, beta, 1)
            if v < beta:
                beta = v
                best_action = a
        return best_action


    def max_value(self, state, alpha, beta, cutoff):
        if cutoff == self.cutoff or self.terminal_test(state):
            return self.utility(state)
        v = -inf
        for a in self.actions(state):
            v = max(v, self.min_value(self.result(state, a), alpha, beta, cutoff+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, alpha, beta, cutoff):
        if cutoff == self.cutoff or self.terminal_test(state):
            return self.utility(state)
        v = inf
        for a in self.actions(state):
            v = min(v, self.max_value(self.result(state, a), alpha, beta, cutoff+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


    def _get_turn(self, state):
        empties = 0
        for row in range(7):
            for col in range(6):
                if state[row][col] == EMPTY:
                    empties += 1
        if empties % 2 == 1:
            return PLAYER1
        else:
            return PLAYER2


    def __check_horizontal_win(self, state):
        win = False
        for row in range(6):
            for col in range(4):
                if state[col][row] != EMPTY:
                    win = (state[col][row] == state[col + 1][row]) and (
                        state[col][row] == state[col + 2][row]) and (
                              state[col][row] == state[col + 3][row])
                if win:
                    return state[col][row]
        return -1

    def __check_vertical_win(self, state):
        win = False
        for col in range(7):
            for row in range(3):
                if state[col][row] != EMPTY:
                    win = (state[col][row] == state[col][row + 1]) and (
                        state[col][row] == state[col][row + 2]) and (
                              state[col][row] == state[col][row + 3])
                if win:
                    return state[col][row]
        return -1

    def __check_neg_diagonal_win(self, state):
        win = False
        for col in range(4):
            for row in range(3):
                if state[col][row] != EMPTY:
                    win = (state[col][row] == state[col + 1][row + 1]) and (
                        state[col][row] == state[col + 2][row + 2]) and (
                              state[col][row] == state[col + 3][row + 3])
                if win:
                    return state[col][row]
        return -1

    def __check_pos_diagonal_win(self, state):
        win = False
        for col in range(3, 7):
            for row in range(3):
                if state[col][row] != EMPTY:
                    win = (state[col][row] == state[col - 1][row + 1]) and (
                        state[col][row] == state[col - 2][row + 2]) and (
                              state[col][row] == state[col - 3][row + 3])
                if win:
                    return state[col][row]
        return -1