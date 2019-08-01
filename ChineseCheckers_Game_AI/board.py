import pygame
from a_star import *
from alphabeta import *
from vision import *

screen = pygame.display.set_mode((960, 720))
pygame.display.set_caption('Chinese Checkers')

a = 480
d = 40
board_list = []
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 200)
red = (200, 0, 0)
light_red = (255, 0, 0)
light_blue = (0, 0, 255)
pink = (255, 200, 200)

visited = []
ai_terminal = []
human_terminal = []



class Player:
    def __init__(self, color):
        self.color = color
        self.checkers = []

        self.last_move = None

    # ai make a move
    def make_move(self):
        if is_mixed() is False:  # use A star
            global device
            move = a_star(self.checkers, ai_terminal, human.checkers)
            
            target = move[0]
            new = move[1]
            print("target, new:", target.pos, new.pos)
            
            pygame.draw.circle(screen, white, target.pos, 20, 0)
            pygame.draw.circle(screen, black, target.pos, 20, 1)
            pygame.draw.circle(screen, blue, new.pos, 20, 0)
            for i in range(10):
                if self.checkers[i].pos == target.pos:
                    self.checkers[i] = new
            print("ai has made a a_star move")
        else:  # use minimax, return the checker object that will be moved (target), and the new checker object (new) or position
            move = alpha_beta(self.checkers, ai_terminal, human_terminal, human.checkers)
            target = move[0]
            new = move[1]
            print("target, new:", target.pos, new.pos)

            pygame.draw.circle(screen, white, target.pos, 20, 0)
            pygame.draw.circle(screen, black, target.pos, 20, 1)
            pygame.draw.circle(screen, blue, new.pos, 20, 0)
            for i in range(10):
                if self.checkers[i].pos == target.pos:
                    self.checkers[i] = new
            print("ai has made a minimax move")

        return target.pos, new.pos

    #  determine a player has a move
    def has_move(self):
        flag = 0
        cnt = 0
        ret = 0
        for i in range(10):
            target_pos = self.checkers[i].pos
            # print("target_pos:", target_pos)
            if get_pos_states(target_pos) == 2:
                flag = 1
                # 如果有变化，更新last_move
                target_pos_cp = target_pos
                ret = i
                cnt += 1
        if cnt != 1:
            flag = 0
        if flag == 1:
            self.last_move = target_pos_cp
            print("****************************************************************************get new move.")
            return True, ret 
        else:
            return False, None



human = Player(red)
ai = Player(blue)

class Checker:

    def __init__(self, pos):
        self.pos = pos
        self.moves = []

    def render(self, color):
        pygame.draw.circle(screen, color, self.pos, 20, 0)

    def selected(self):
        pygame.draw.circle(screen, light_red, self.pos, 20, 0)
        # show possible moves
        human_list = []
        ai_list = []
        for i in range(len(human.checkers)):
            human_list.append(human.checkers[i].pos)
        for i in range(len(ai.checkers)):
            ai_list.append(ai.checkers[i].pos)

        self.moves = []
        self.possible_moves(self.pos, False, 0, ai_list, human_list)

        for i in range(len(self.moves)):
            pygame.draw.circle(screen, pink, self.moves[i], 20, 0)
            pygame.draw.circle(screen, black, self.moves[i], 20, 1)

    def unselected(self):
        pygame.draw.circle(screen, red, self.pos, 20, 0)
        # clear possible moves
        for i in range(len(self.moves)):
            pygame.draw.circle(screen, white, self.moves[i], 20, 0)
            pygame.draw.circle(screen, black, self.moves[i], 20, 1)

    def move(self, new_pos):
        pygame.draw.circle(screen, white, self.pos, 20, 0)
        pygame.draw.circle(screen, black, self.pos, 20, 1)
        pygame.draw.circle(screen, red, new_pos, 20, 0)
        self.pos = new_pos
        # clear possible moves except the new_pos
        for i in range(len(self.moves)):
            if self.moves[i] != new_pos:
                pygame.draw.circle(screen, white, self.moves[i], 20, 0)
                pygame.draw.circle(screen, black, self.moves[i], 20, 1)
        self.moves = []

    def possible_moves(self, pos, hop, mode, ai_list, human_list):
        global visited
        if mode == 0:
            visited = []

        x = pos[0]
        y = pos[1]

        # check top_left
        if is_free((x - 22, y - 40), ai_list, human_list) and hop is False:
            self.moves.append((x - 22, y - 40))
        elif ((x - 22, y - 40) in human_list or (x - 22, y - 40) in ai_list) and (
            x - 22, y - 40) not in visited:
            visited.append((x - 22, y - 40))
            if is_free((x - 22 * 2, y - 40 * 2), ai_list, human_list):
                self.moves.append((x - 22 * 2, y - 40 * 2))
                self.possible_moves((x - 22 * 2, y - 40 * 2), True, 1, ai_list, human_list)

        # check top_right
        if is_free((x + 22, y - 40), ai_list, human_list) and hop is False:
            self.moves.append((x + 22, y - 40))
        elif ((x + 22, y - 40) in human_list or (x + 22, y - 40) in ai_list) and (
            x + 22, y - 40) not in visited:
            visited.append((x + 22, y - 40))
            if is_free((x + 22 * 2, y - 40 * 2), ai_list, human_list):
                self.moves.append((x + 22 * 2, y - 40 * 2))
                self.possible_moves((x + 22 * 2, y - 40 * 2), True, 1, ai_list, human_list)

        # check left
        if is_free((x - 44, y), ai_list, human_list) and hop is False:
            self.moves.append((x - 44, y))
        elif ((x - 44, y) in human_list or (x - 44, y) in ai_list) and (x - 44, y) not in visited:
            visited.append((x - 44, y))
            if is_free((x - 44 * 2, y), ai_list, human_list):
                self.moves.append((x - 44 * 2, y))
                self.possible_moves((x - 44 * 2, y), True, 1, ai_list, human_list)

        # check right
        if is_free((x + 44, y), ai_list, human_list) and hop is False:
            self.moves.append((x + 44, y))
        elif ((x + 44, y) in human_list or (x + 44, y) in ai_list) and (x + 44, y) not in visited:
            visited.append((x + 44, y))
            if is_free((x + 44 * 2, y), ai_list, human_list):
                self.moves.append((x + 44 * 2, y))
                self.possible_moves((x + 44 * 2, y), True, 1, ai_list, human_list)

        # check down_left
        if is_free((x - 22, y + 40), ai_list, human_list) and hop is False:
            self.moves.append((x - 22, y + 40))
        elif ((x - 22, y + 40) in human_list or (x - 22, y + 40) in ai_list) and (
            x - 22, y + 40) not in visited:
            visited.append((x - 22, y + 40))
            if is_free((x - 22 * 2, y + 40 * 2), ai_list, human_list):
                self.moves.append((x - 22 * 2, y + 40 * 2))
                self.possible_moves((x - 22 * 2, y + 40 * 2), True, 1, ai_list, human_list)

        # check down_right
        if is_free((x + 22, y + 40), ai_list, human_list) and hop is False:
            self.moves.append((x + 22, y + 40))
        elif ((x + 22, y + 40) in human_list or (x + 22, y + 40) in ai_list) and (
            x + 22, y + 40) not in visited:
            visited.append((x + 22, y + 40))
            if is_free((x + 22 * 2, y + 40 * 2), ai_list, human_list):
                self.moves.append((x + 22 * 2, y + 40 * 2))
                self.possible_moves((x + 22 * 2, y + 40 * 2), True, 1, ai_list, human_list)

    def best_vertical_move(self):
        if self is human:  # find the largest y
            ymax = 0
            for i in range(len(self.moves)):
                if self.moves[i][1] > ymax:
                    ymax = self.moves[i][1]
            return ymax
        else:  # find the smallest y
            ymin = 700
            for i in range(len(self.moves)):
                if self.moves[i][1] < ymin:
                    ymin = self.moves[i][1]
            return ymin


# static methods
def init_board():
    for i in range(0, 4):
        for j in range(i+1):
            board_list.append((a - 22 * i + 44 * j, d * (i + 1)))
    for i in range(4, 9):
        for j in range(17-i):
            board_list.append((a - 22 * (16-i) + 44 * j, d * (i + 1)))
    for i in range(9, 13):
        for j in range(i+1):
            board_list.append((a - 22 * i + 44 * j, d * (i + 1)))
    for i in range(13, 17):
        for j in range(17-i):
            board_list.append((a - 22 * (16-i) + 44 * j, d * (i + 1)))

def draw_board():
    screen.fill(white)
    for i in range(len(board_list)):
        pygame.draw.circle(screen, black, board_list[i], 20, 1)

def init_checkers():
    global ai_terminal, human_terminal

    for i in range(10):
        piece = Checker(board_list[i])
        ai_terminal.append(piece)
    for i in reversed(range(len(board_list)-10, len(board_list))):
        piece = Checker(board_list[i])
        human_terminal.append(piece)

    human.checkers = []
    ai.checkers = []
    for i in range(10):
        piece = Checker(board_list[i])
        piece.render(human.color)
        human.checkers.append(piece)
    for i in reversed(range(len(board_list)-10, len(board_list))):
        piece = Checker(board_list[i])
        piece.render(ai.color)
        ai.checkers.append(piece)

def is_free(pos, ai_list, human_list):
    if pos in board_list and pos not in human_list and pos not in ai_list:
        return True
    else:
        return False

def is_mixed():
    human_max = 0
    ai_min = 700
    human_min = 700
    ai_max = 0

    for i in range(10):
        if human.checkers[i].pos[1] > human_max:
            human_max = human.checkers[i].pos[1]
        if ai.checkers[i].pos[1] < ai_min:
            ai_min = ai.checkers[i].pos[1]

    for i in range(10):
        if human.checkers[i].pos[1] < human_min:
            human_min = human.checkers[i].pos[1]
        if ai.checkers[i].pos[1] > ai_max:
            ai_max = ai.checkers[i].pos[1]

    if (human_min < ai_min and (ai_min - human_max) > 120) or (ai_min < human_min and (human_min - ai_max) > 0):  # no interactions
        return False
    else:
        return True


