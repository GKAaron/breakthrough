import collections as cl
import random as rd
from copy import deepcopy
MIN = -1000
MAX = 1000
NODE1 = 0
NODE2 = 0
NODE3 = 0
NODE4 = 0


class Chess:
    def __init__(self, c: str, hori: str, vert: int):
        self.type = c
        self.hori = hori
        self.vert = vert


class Board:
    def __init__(self):
        #
        self.board = []
        self.white = set()
        self.black = set()
        self.board_ini()
        #
        self.chess_num = {'w': 16, 'b': 16}
        self.white_horizon = cl.OrderedDict()
        self.black_horizon = cl.OrderedDict()
        self.horizon_ini()
        self.white_vertical = cl.OrderedDict()
        self.black_vertical = cl.OrderedDict()
        self.vertical_ini()
        self.cap_w = dict()
        self.cap_b = dict()
        self.b_w = 6
        self.w_b = 6
        self.w_dis = 1
        self.b_dis = 1
        self.w_single_num = 0
        self.b_single_num = 0
        self.w_gap = 0
        self.w_gap_num = 0
        self.b_gap = 0
        self.b_gap_num = 0
        self.w_frontier = 6
        self.w_back = 7
        self.b_frontier = 1
        self.b_back = 0
        self.w_single = set()
        self.b_single = set()

    def board_ini(self):
        #
        i = 0
        while i < 2:
            self.board.append(['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'])
            i += 1
        while 1 < i < 6:
            self.board.append(['0', '0', '0', '0', '0', '0', '0', '0'])
            i += 1
        while 5 < i < 8:
            self.board.append(['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'])
            i += 1
            #
        self.white = {('a', 6), ('a', 7), ('b', 6), ('b', 7), ('c', 6), ('c', 7), ('d', 6), ('d', 7),
                      ('e', 6), ('e', 7), ('f', 6), ('f', 7), ('g', 6), ('g', 7), ('h', 6), ('h', 7)}
        self.black = {('a', 0), ('a', 1), ('b', 0), ('b', 1), ('c', 0), ('c', 1), ('d', 0), ('d', 1),
                      ('e', 0), ('e', 1), ('f', 0), ('f', 1), ('g', 0), ('g', 1), ('h', 0), ('h', 1)}

    def player_num(self, c: str):
        return self.chess_num[c]

    def opponent_num(self, c: str):
        if 'w' == c:
            return self.chess_num['b']
        else:
            return self.chess_num['w']

    def player_chess(self, c:str):
        if 'w' == c:
            return self.white
        else:
            return self.black

    def horizon_ini(self):
        i = 97
        while i < 105:
            self.white_horizon[chr(i)] = [7, 6]
            self.black_horizon[chr(i)] = [0, 1]
            i += 1

    def vertical_ini(self):
        i = 0
        while i < 2:
            self.black_vertical[i] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
            self.white_vertical[i] = []
            i += 1
        while 1 < i < 6:
            self.white_vertical[i] = []
            self.black_vertical[i] = []
            i += 1
        while 5 < i < 8:
            self.white_vertical[i] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
            self.black_vertical[i] = []
            i += 1

    def posi_act(self,c: str, hori: str, vert: int)->list:
        posi_act = []
        if 'w' == c:
            i = ord(hori)-1
            j = ord(hori)+1
            if i >= 97:
                if (chr(i),vert-1) not in self.white:
                    posi_act.append((chr(i), vert-1))
            if j <= 104:
                if (chr(j),vert-1) not in self.white:
                    posi_act.append((chr(j), vert-1))
            if (hori,vert-1) not in self.white and (hori,vert-1) not in self.black:
                posi_act.append((hori, vert-1))
        else:
            i = ord(hori) - 1
            j = ord(hori) + 1
            if i >= 97:
                if (chr(i),vert+1) not in self.black:
                    posi_act.append((chr(i), vert+1))
            if j <= 104:
                if (chr(j),vert+1) not in self.black:
                    posi_act.append((chr(j), vert+1))
            if (hori,vert+1) not in self.black and (hori,vert+1) not in self.white:
                posi_act.append((hori, vert+1))
        return posi_act

    def unstable(self,c: str, hori: str, vert: int):
        if 'w' == c:
            i = ord(hori) - 1
            j = ord(hori) + 1
            if i >= 97:
                if (chr(i),vert-1) in self.black:
                    if (hori, vert) not in self.cap_w.keys():
                        self.cap_w[(hori, vert)] = [(chr(i), vert-1)]
                    else:
                        self.cap_w[(hori, vert)].append((chr(i), vert-1))
                    if (chr(i), vert-1) not in self.cap_b.keys():
                        self.cap_b[(chr(i), vert-1)] = [(hori, vert)]
                    else:
                        self.cap_b[(chr(i), vert-1)].append((hori, vert))
            if j <= 104:
                if (chr(j),vert-1) in self.black:
                    if (hori, vert) not in self.cap_w.keys():
                        self.cap_w[(hori, vert)] = [(chr(j), vert-1)]
                    else:
                        self.cap_w[(hori, vert)].append((chr(j), vert-1))
                    if (chr(j), vert - 1) not in self.cap_b.keys():
                        self.cap_b[(chr(j), vert-1)] = [(hori, vert)]
                    else:
                        self.cap_b[(chr(j), vert-1)].append((hori, vert))
        else:
            i = ord(hori) - 1
            j = ord(hori) + 1
            if i >= 97:
                if (chr(i),vert+1) in self.white:
                    if (hori, vert) not in self.cap_b.keys():
                        self.cap_b[(hori, vert)] = [(chr(i), vert+1)]
                    else:
                        self.cap_b[(hori, vert)].append((chr(i), vert+1))
                    if (chr(i), vert+1) not in self.cap_w.keys():
                        self.cap_w[(chr(i), vert+1)] = [(hori, vert)]
                    else:
                        self.cap_w[(chr(i), vert+1)].append((hori, vert))
            if j <= 104:
                if (chr(j),vert+1) in self.white:
                    if (hori, vert) not in self.cap_b.keys():
                        self.cap_b[(hori, vert)] = [(chr(j), vert+1)]
                    else:
                        self.cap_b[(hori, vert)].append((chr(j), vert+1))
                    if (chr(j), vert+1) not in self.cap_w.keys():
                        self.cap_w[(chr(j), vert+1)] = [(hori, vert)]
                    else:
                        self.cap_w[(chr(j), vert+1)].append((hori, vert))
        if self.cap_b:
            return True
        else:
            return False

    def single_check(self,c: str, hori: str, vert: int):
        if 'w' == c:
            if (chr(ord(hori)-1), vert) not in self.white and (chr(ord(hori)+1), vert) not in self.white:
                self.w_single.add((hori,vert))
                return True
            else:
                return False
        else:
            if (chr(ord(hori)-1), vert) not in self.black and (chr(ord(hori)+1), vert) not in self.black:
                self.b_single.add((hori,vert))
                return True
            else:
                return False

    def update_white_single(self, hori: str, vert: int, tar_hori: str, tar_vert: int):
        # update white single, self old
        if (hori, vert) in self.w_single:
            self.w_single.remove((hori, vert))
            self.w_single_num -= 1
        # update white single, self old neighbor
        if vert < self.w_back:
            if (chr(ord(hori) - 1), vert) in self.white:
                if self.single_check('w', chr(ord(hori) - 1), vert):
                    self.w_single_num += 1
            if (chr(ord(hori) + 1), vert) in self.white:
                if self.single_check('w', chr(ord(hori) + 1), vert):
                    self.w_single_num += 1
        # update white single,self
        if self.single_check('w', tar_hori, tar_vert):
            self.w_single_num += 1
        # update white single,self neighbor
        else:
            if (chr(ord(tar_hori) - 1), tar_vert) in self.w_single:
                self.w_single.remove((chr(ord(tar_hori) - 1), tar_vert))
                self.w_single_num -= 1
            if (chr(ord(tar_hori) + 1), tar_vert) in self.w_single:
                self.w_single.remove((chr(ord(tar_hori) + 1), tar_vert))
                self.w_single_num -= 1

    def update_black_single(self, hori: str, vert: int, tar_hori: str, tar_vert: int):
        if (hori, vert) in self.b_single:
            self.b_single.remove((hori, vert))
            self.b_single_num -= 1
        # update black single, self old neighbor
        if vert > self.b_back:
            if (chr(ord(hori) - 1), vert) in self.black:
                if self.single_check('b', chr(ord(hori) - 1), vert):
                    self.b_single_num += 1
            if (chr(ord(hori) + 1), vert) in self.black:
                if self.single_check('b', chr(ord(hori) + 1), vert):
                    self.b_single_num += 1
        # update black single,self
        if self.single_check('b', tar_hori, tar_vert):
            self.b_single_num += 1
        # update black single,self neighbor
        else:
            if (chr(ord(tar_hori) - 1), tar_vert) in self.b_single:
                self.b_single.remove((chr(ord(tar_hori) - 1), tar_vert))
                self.b_single_num -= 1
            if (chr(ord(tar_hori) + 1), tar_vert) in self.b_single:
                self.b_single.remove((chr(ord(tar_hori) + 1), tar_vert))
                self.b_single_num -= 1

    def cal_gap(self, c: str, hori: str)->tuple:
        if 'w' == c:
            length = len(self.white_horizon[hori])
            if length <= 1:
                return 0, 0
            else:
                gap_num = 0
                gap = self.white_horizon[hori][0] - self.white_horizon[hori][-1] - length + 1
                if gap > 0:
                    gap_num = 1
                return gap, gap_num
        else:
            length = len(self.black_horizon[hori])
            if length <= 1:
                return 0, 0
            else:
                gap_num = 0
                gap = self.black_horizon[hori][-1] - self.black_horizon[hori][0] - length + 1
                if gap > 0:
                    gap_num = 1
                return gap, gap_num

    def update_white_horizon(self, hori: str, vert: int, tar_hori: str, tar_vert: int):
        self.white_horizon[hori].sort(reverse=True)
        self.white_horizon[tar_hori].sort(reverse=True)
        # check white_horizon_old
        old_gap_h,old_gap_num_h = self.cal_gap('w', hori)
        old_gap_t,old_gap_num_t = self.cal_gap('w', tar_hori)
        #
        self.white_horizon[hori].remove(vert)
        self.white_horizon[tar_hori].append(tar_vert)
        # check white_horizon_new
        new_gap_h, new_gap_num_h = self.cal_gap('w', hori)
        new_gap_t, new_gap_num_t = self.cal_gap('w', tar_hori)
        if hori != tar_hori:
            self.w_gap = self.w_gap - old_gap_h - old_gap_t + new_gap_h + new_gap_t
            self.w_gap_num = self.w_gap_num - old_gap_num_h - old_gap_num_t + new_gap_num_h + new_gap_num_t
        else:
            self.w_gap = self.w_gap - old_gap_h + new_gap_h
            self.w_gap_num = self.w_gap_num - old_gap_num_h + new_gap_num_h

    def update_black_horizon(self, hori: str, vert: int, tar_hori: str, tar_vert: int):
        self.black_horizon[hori].sort()
        self.black_horizon[tar_hori].sort()
        # check black_horizon_old
        old_gap_h,old_gap_num_h = self.cal_gap('b', hori)
        old_gap_t,old_gap_num_t = self.cal_gap('b', tar_hori)
        #
        self.black_horizon[hori].remove(vert)
        self.black_horizon[tar_hori].append(tar_vert)
        # check black_horizon_new
        new_gap_h, new_gap_num_h = self.cal_gap('b', hori)
        new_gap_t, new_gap_num_t = self.cal_gap('b', tar_hori)
        if hori != tar_hori:
            self.b_gap = self.b_gap - old_gap_h - old_gap_t + new_gap_h + new_gap_t
            self.b_gap_num = self.b_gap_num - old_gap_num_h - old_gap_num_t + new_gap_num_h + new_gap_num_t
        else:
            self.b_gap = self.b_gap - old_gap_h + new_gap_h
            self.b_gap_num = self.b_gap_num - old_gap_num_h + new_gap_num_h

    def update_white_vertical(self, hori: str, vert: int, tar_hori: str, tar_vert: int):
        self.white_vertical[vert].remove(hori)
        self.white_vertical[tar_vert].append(tar_hori)
        if tar_vert < self.w_frontier:
            self.w_frontier -= 1
            self.w_b -= 1
            self.w_dis += 1
        if vert == self.w_back:
            if 0 == len(self.white_vertical[vert]):
                self.w_dis -= 1
                self.w_back -= 1

    def update_black_vertical(self, hori: str, vert: int, tar_hori: str, tar_vert: int):
        self.black_vertical[vert].remove(hori)
        self.black_vertical[tar_vert].append(tar_hori)
        if tar_vert > self.b_frontier:
            self.b_frontier += 1
            self.b_w -= 1
            self.b_dis += 1
        if vert == self.b_back:
            if 0 == len(self.black_vertical[vert]):
                self.b_dis -= 1
                self.b_back -= 1

    def cap_update_black(self, hori: str, vert: int):
        # black update single
        if (hori, vert) in self.b_single:
            self.b_single.remove((hori, vert))
            self.b_single_num -= 1
        # update black single, self neighbor
        if vert > self.b_back:
            if (chr(ord(hori) - 1), vert) in self.black:
                if self.single_check('b', chr(ord(hori) - 1), vert):
                    self.b_single_num += 1
            if (chr(ord(hori) + 1), vert) in self.black:
                if self.single_check('b', chr(ord(hori) + 1), vert):
                    self.b_single_num += 1
        # black update horizon
        old_gap_h,old_gap_num_h = self.cal_gap('b', hori)
        self.black_horizon[hori].remove(vert)
        new_gap_h, new_gap_num_h = self.cal_gap('b', hori)
        self.b_gap = self.b_gap - old_gap_h + new_gap_h
        self.b_gap_num = self.b_gap_num - old_gap_h + new_gap_num_h
        # black update vertical
        self.black_vertical[vert].remove(hori)
        if vert == self.b_frontier:
            if len(self.black_vertical[vert]) == 0:
                i = vert - 1
                while i in self.black_vertical.keys():
                    if len(self.black_vertical[i]) > 0:
                        self.b_frontier = i
                        self.b_w = 7 - self.b_frontier
                        self.b_dis = self.b_frontier - self.b_back
                        break
                    i -= 1
        if vert == self.b_back:
            if 0 == len(self.black_vertical[vert]):
                i = vert + 1
                while i in self.black_vertical.keys():
                    if len(self.black_vertical[i]) > 0:
                        self.b_back = i
                        self.b_dis = self.b_frontier - self.b_back
                        break
                    i += 1

    def cap_update_white(self, hori: str, vert: int):
        # update white single, self
        if (hori, vert) in self.w_single:
            self.w_single.remove((hori, vert))
            self.w_single_num -= 1
        # update white single, self neighbor
        if vert < self.w_back:
            if (chr(ord(hori) - 1), vert) in self.white:
                if self.single_check('w', chr(ord(hori) - 1), vert):
                    self.w_single_num += 1
            if (chr(ord(hori) + 1), vert) in self.white:
                if self.single_check('w', chr(ord(hori) + 1), vert):
                    self.w_single_num += 1
        # update white horizon
        old_gap_h, old_gap_num_h = self.cal_gap('w', hori)
        self.white_horizon[hori].remove(vert)
        new_gap_h, new_gap_num_h = self.cal_gap('w', hori)
        self.w_gap = self.w_gap - old_gap_h + new_gap_h
        self.w_gap_num = self.w_gap_num - old_gap_num_h + new_gap_num_h
        # white update vertical
        self.white_vertical[vert].remove(hori)
        if vert == self.w_frontier:
            if len(self.white_vertical[vert]) == 0:
                i = vert + 1
                while i in self.white_vertical.keys():
                    if len(self.white_vertical[i]) > 0:
                        self.w_frontier = i
                        self.w_b = self.w_frontier
                        self.w_dis = self.w_back - self.w_frontier
                        break
                    i += 1
        if vert == self.w_back:
            if 0 == len(self.white_vertical[vert]):
                i = vert - 1
                while i in self.white_vertical.keys():
                    if len(self.white_vertical[i]) > 0:
                        self.w_back = i
                        self.w_dis = self.w_back - self.w_frontier
                        break
                    i -= 1

    def move(self, c: str, hori: str, vert: int, tar_hori: str, tar_vert: int):
        if 'w' == c:
            # update white
            self.white.remove((hori,vert))
            self.white.add((tar_hori,tar_vert))
            self.update_white_single(hori,vert,tar_hori,tar_vert)
            self.update_white_horizon(hori,vert,tar_hori,tar_vert)
            self.board[vert][ord(hori)-97] = '0'
            self.board[tar_vert][ord(tar_hori)-97] = 'w'
            self.update_white_vertical(hori,vert,tar_hori,tar_vert)
            # capture happens
            if (tar_hori,tar_vert) in self.black:
                self.chess_num['b'] -= 1
                self.black.remove((tar_hori, tar_vert))
                self.cap_update_black(tar_hori, tar_vert)
                return True
            else:
                return False
        else:
            # update black
            self.black.remove((hori,vert))
            self.black.add((tar_hori,tar_vert))
            self.update_black_single(hori,vert,tar_hori,tar_vert)
            self.update_black_horizon(hori, vert, tar_hori, tar_vert)
            self.board[vert][ord(hori)-97] = '0'
            self.board[tar_vert][ord(tar_hori)-97] = 'b'
            self.update_black_vertical(hori, vert, tar_hori, tar_vert)
            # capture happens
            if (tar_hori,tar_vert) in self.white:
                self.chess_num['w'] -= 1
                self.white.remove((tar_hori, tar_vert))
                self.cap_update_white(tar_hori, tar_vert)
                return True
            else:
                return False


class OffPlayer:
    def __init__(self, type: str):
        if type == 'w':
            self.type = type
            self.oppo = 'b'
        else:
            self.type = type
            self.oppo = 'w'

    def off_eva1(self, board:Board):
        opp_num = board.opponent_num(self.type)
        v = 2*(30-opp_num)+ rd.random()
        # opp_num = board.opponent_num(self.type)
        # sel_num = board.player_num(self.type)
        # if self.type == 'w':
        #     gap = board.w_gap
        #     gap_num = board.w_gap_num
        #     dis = board.w_b
        # else:
        #     gap = board.b_gap
        #     gap_num = board.b_gap_num
        #     dis = board.b_w
        # if dis == 0:
        #     v = 6*sel_num + 10*(16-opp_num) + 0.3*gap - 0.1*gap_num + 40
        # else:
        #     v = 6*sel_num + 10*(16-opp_num) + 0.3*gap - 0.1*gap_num + 40/dis
        return v

    def move(self, board: Board):
        best = self.minimax_search(board)
        hori = best[0][0]
        vert = best[0][1]
        tar_hori = best[1][0]
        tar_vert = best[1][1]
        board.move(self.type,hori,vert,tar_hori,tar_vert)

    def max_search(self, depth, board:Board):
        if board.b_w == 0:
            if self.type == 'b':
                return self.off_eva1(board) + 400
            else:
                return self.off_eva1(board) - 400
        elif board.w_b == 0:
            if self.type == 'w':
                return self.off_eva1(board) + 400
            else:
                return self.off_eva1(board) - 400
        elif depth == 0:
            return self.off_eva1(board)
        cap = None
        v = MIN
        for hori,vert in board.player_chess(self.type):
            posi_act = board.posi_act(self.type,hori,vert)
            for tar_hori,tar_vert in posi_act:
                new_board = deepcopy(board)
                global NODE1
                NODE1 += 1
                if new_board.move(self.type,hori,vert,tar_hori,tar_vert):
                    cap = self.oppo
                v = max(v,self.min_search(depth-1,new_board))
        return v

    def min_search(self, depth, board: Board):
        if board.b_w == 0:
            if self.type == 'b':
                return self.off_eva1(board) + 400
            else:
                return self.off_eva1(board) - 400
        elif board.w_b == 0:
            if self.type == 'w':
                return self.off_eva1(board) + 400
            else:
                return self.off_eva1(board) - 400
        elif depth == 0:
            return self.off_eva1(board)
        cap = None
        v = MAX
        for hori, vert in board.player_chess(self.oppo):
            posi_act = board.posi_act(self.oppo, hori, vert)
            for tar_hori, tar_vert in posi_act:
                new_board = deepcopy(board)
                global NODE1
                NODE1 += 1
                if new_board.move(self.oppo, hori, vert, tar_hori, tar_vert):
                    cap = self.type
                v = min(v, self.max_search(depth - 1, new_board))
        return v

    def minimax_search(self, board:Board, depth=3):
        cap = None
        v = MIN
        for hori,vert in board.player_chess(self.type):
            posi_act = board.posi_act(self.type,hori,vert)
            for tar_hori,tar_vert in posi_act:
                new_board = deepcopy(board)
                global NODE1
                NODE1 += 1
                if new_board.move(self.type,hori,vert,tar_hori,tar_vert):
                    cap = self.oppo
                value = self.min_search(depth-1,new_board)
                if v < value:
                    v = value
                    move = [(hori,vert),(tar_hori,tar_vert)]
        return move


class DefPlayer:
    def __init__(self, type: str):
        if type == 'w':
            self.type = type
            self.oppo = 'b'
        else:
            self.type = type
            self.oppo = 'w'

    def def_eva1(self, board:Board):
        # sel_num = board.player_num(self.type)
        # v = 2*sel_num + rd.random()
        opp_num = board.opponent_num(self.type)
        sel_num = board.player_num(self.type)
        if self.type == 'w':
            gap = board.w_gap
            dis = board.b_w
            inter = board.w_dis
            single_num = board.w_single_num
        else:
            gap = board.b_gap
            dis = board.w_b
            inter = board.b_dis
            single_num = board.b_single_num
        v = 20*sel_num - 10*opp_num + 2*dis - (inter-1) - 0.3*gap - 0.2*single_num
        return v

    def move(self, board: Board):
        best = self.minimax_search(board)
        hori = best[0][0]
        vert = best[0][1]
        tar_hori = best[1][0]
        tar_vert = best[1][1]
        board.move(self.type,hori,vert,tar_hori,tar_vert)

    def max_search(self, depth, board:Board):
        if board.b_w == 0:
            if self.type == 'b':
                return self.def_eva1(board) + 400
            else:
                return self.def_eva1(board) - 400
        elif board.w_b == 0:
            if self.type == 'w':
                return self.def_eva1(board) + 400
            else:
                return self.def_eva1(board) - 400
        elif depth == 0:
            return self.def_eva1(board)
        cap = None
        v = MIN
        for hori,vert in board.player_chess(self.type):
            posi_act = board.posi_act(self.type,hori,vert)
            for tar_hori,tar_vert in posi_act:
                new_board = deepcopy(board)
                global NODE2
                NODE2 += 1
                if new_board.move(self.type,hori,vert,tar_hori,tar_vert):
                    cap = self.oppo
                v = max(v,self.min_search(depth-1,new_board))
        return v

    def min_search(self, depth, board: Board):
        if board.b_w == 0:
            if self.type == 'b':
                return self.def_eva1(board) + 400
            else:
                return self.def_eva1(board) - 400
        elif board.w_b == 0:
            if self.type == 'w':
                return self.def_eva1(board) + 400
            else:
                return self.def_eva1(board) - 400
        elif depth == 0:
            return self.def_eva1(board)
        cap = None
        v = MAX
        for hori, vert in board.player_chess(self.oppo):
            posi_act = board.posi_act(self.oppo, hori, vert)
            for tar_hori, tar_vert in posi_act:
                new_board = deepcopy(board)
                global NODE2
                NODE2 += 1
                if new_board.move(self.oppo, hori, vert, tar_hori, tar_vert):
                    cap = self.type
                v = min(v, self.max_search(depth - 1, new_board))
        return v

    def minimax_search(self, board:Board, depth=3):
        cap = None
        v = MIN
        for hori,vert in board.player_chess(self.type):
            posi_act = board.posi_act(self.type,hori,vert)
            for tar_hori,tar_vert in posi_act:
                new_board = deepcopy(board)
                global NODE2
                NODE2 += 1
                if new_board.move(self.type,hori,vert,tar_hori,tar_vert):
                    cap = self.oppo
                value = self.min_search(depth-1,new_board)
                if v < value:
                    v = value
                    move = [(hori,vert),(tar_hori,tar_vert)]
        return move


class OffPlayer2:
    def __init__(self, type: str):
        if type == 'w':
            self.type = type
            self.oppo = 'b'
        else:
            self.type = type
            self.oppo = 'w'

    def off_eva1(self, board:Board):
        opp_num = board.opponent_num(self.type)
        sel_num = board.player_num(self.type)
        if self.type == 'w':
            gap = board.w_gap
            gap_num = board.w_gap_num
            dis = board.w_b
        else:
            gap = board.b_gap
            gap_num = board.b_gap_num
            dis = board.b_w
        if dis == 0:
            v = 6*sel_num + 10*(16-opp_num) + 0.3*gap - 0.1*gap_num + 40
        else:
            v = 6*sel_num + 10*(16-opp_num) + 0.3*gap - 0.1*gap_num + 40/dis
        return v

    def move(self, board: Board):
        best = self.minimax_search(board)
        hori = best[0][0]
        vert = best[0][1]
        tar_hori = best[1][0]
        tar_vert = best[1][1]
        board.move(self.type,hori,vert,tar_hori,tar_vert)

    def max_search(self, depth, board:Board, x, y, best_move:list):
        if board.b_w == 0:
            if self.type == 'b':
                return self.off_eva1(board) + 400,[]
            else:
                return self.off_eva1(board) - 400,[]
        elif board.w_b == 0:
            if self.type == 'w':
                return self.off_eva1(board) + 400,[]
            else:
                return self.off_eva1(board) - 400,[]
        elif depth == 0:
            return self.off_eva1(board),[]
        cap = None
        v = MIN
        best=[]
        global NODE3
        if best_move:
            mov = best_move.pop()
            hori,vert = mov[0]
            tar_hori,tar_vert = mov[1]
            new_board = deepcopy(board)
            NODE3 += 1
            new_board.move(self.type, hori, vert, tar_hori, tar_vert)
            value,sub_best = self.min_search(depth - 1, new_board,x,y,best_move)
            if value > v:
                v = value
                sub_best.append(((hori, vert),(tar_hori, tar_vert)))
                best = sub_best
            if v >= y:
                return v,[]
            x = max(x,v)
        for hori,vert in board.player_chess(self.type):
            posi_act = board.posi_act(self.type,hori,vert)
            for tar_hori,tar_vert in posi_act:
                new_board = deepcopy(board)
                NODE3 += 1
                if new_board.move(self.type,hori,vert,tar_hori,tar_vert):
                    cap = self.oppo
                value,sub_best = self.min_search(depth-1,new_board,x,y,[])
                if value > v:
                    v = value
                    sub_best.append(((hori, vert), (tar_hori, tar_vert)))
                    best = sub_best
                if v >= y:
                    return v,[]
                x = max(x, v)
        return v,best

    def min_search(self, depth, board: Board, x, y, best_move:list):
        if board.b_w == 0:
            if self.type == 'b':
                return self.off_eva1(board) + 400,[]
            else:
                return self.off_eva1(board) - 400,[]
        elif board.w_b == 0:
            if self.type == 'w':
                return self.off_eva1(board) + 400,[]
            else:
                return self.off_eva1(board) - 400,[]
        elif depth == 0:
            return self.off_eva1(board),[]
        cap = None
        v = MAX
        best =[]
        global NODE3
        if best_move:
            mov = best_move.pop()
            hori,vert = mov[0]
            tar_hori,tar_vert = mov[1]
            new_board = deepcopy(board)
            NODE3 += 1
            new_board.move(self.oppo, hori, vert, tar_hori, tar_vert)
            value,sub_best = self.max_search(depth - 1, new_board,x,y,best_move)
            if v > value:
                v = value
                sub_best.append(((hori,vert),(tar_hori,tar_vert)))
                best = sub_best
            if v <= x:
                return v,[]
            y = min(y,v)
        for hori, vert in board.player_chess(self.oppo):
            posi_act = board.posi_act(self.oppo, hori, vert)
            for tar_hori, tar_vert in posi_act:
                new_board = deepcopy(board)
                NODE3 += 1
                if new_board.move(self.oppo, hori, vert, tar_hori, tar_vert):
                    cap = self.type
                value, sub_best = self.max_search(depth - 1, new_board, x, y, [])
                if v > value:
                    v = value
                    sub_best.append(((hori, vert), (tar_hori, tar_vert)))
                    best = sub_best
                if v < x:
                    return v,[]
                y = min(y,v)
        return v,best

    def minimax_search(self, board:Board, max_depth=4):
        depth = 1
        best_move = []
        global NODE3
        while depth <= max_depth:
            cap = None
            x = MIN
            y = MAX
            v = MIN
            if best_move:
                best = best_move.pop()
                hori,vert = best[0]
                tar_hori,tar_vert = best[1]
                new_board = deepcopy(board)
                NODE3 += 1
                new_board.move(self.type,hori,vert,tar_hori,tar_vert)
                value,sub_best = self.min_search(depth-1,new_board,x,y,best_move)
                if value > v:
                    v = value
                    sub_best.append(((hori,vert),(tar_hori,tar_vert)))
                    best_move = sub_best
            for hori,vert in board.player_chess(self.type):
                posi_act = board.posi_act(self.type,hori,vert)
                for tar_hori,tar_vert in posi_act:
                    new_board = deepcopy(board)
                    NODE3 += 1
                    if new_board.move(self.type,hori,vert,tar_hori,tar_vert):
                        cap = self.oppo
                    value,sub_best = self.min_search(depth-1,new_board,x,y,[])
                    if v < value:
                        v = value
                        sub_best.append(((hori,vert),(tar_hori,tar_vert)))
                        best_move = sub_best
            depth += 1
        move = best_move.pop()
        return move


class DefPlayer2:
    def __init__(self, type: str):
        if type == 'w':
            self.type = type
            self.oppo = 'b'
        else:
            self.type = type
            self.oppo = 'w'

    def def_eva1(self, board:Board):
        # opp_num = board.opponent_num(self.type)
        # sel_num = board.player_num(self.type)
        # if self.type == 'w':
        #     gap = board.w_gap
        #     dis = board.b_w
        #     inter = board.w_dis
        #     single_num = board.w_single_num
        # else:
        #     gap = board.b_gap
        #     dis = board.w_b
        #     inter = board.b_dis
        #     single_num = board.b_single_num
        # v = 20*sel_num - 10*opp_num + 2*dis - (inter-1) - 0.3*gap - 0.2*single_num
        sel_num = board.player_num(self.type)
        v = 2*sel_num + rd.random()
        return v

    def move(self, board: Board):
        best = self.minimax_search(board)
        hori = best[0][0]
        vert = best[0][1]
        tar_hori = best[1][0]
        tar_vert = best[1][1]
        board.move(self.type,hori,vert,tar_hori,tar_vert)

    def max_search(self, depth, board:Board, x, y, best_move:list):
        if board.b_w == 0:
            if self.type == 'b':
                return self.def_eva1(board) + 400,[]
            else:
                return self.def_eva1(board) - 400,[]
        elif board.w_b == 0:
            if self.type == 'w':
                return self.def_eva1(board) + 400,[]
            else:
                return self.def_eva1(board) - 400,[]
        elif depth == 0:
            return self.def_eva1(board),[]
        cap = None
        v = MIN
        best=[]
        global NODE4
        if best_move:
            mov = best_move.pop()
            hori,vert = mov[0]
            tar_hori,tar_vert = mov[1]
            new_board = deepcopy(board)
            NODE4 += 1
            new_board.move(self.type, hori, vert, tar_hori, tar_vert)
            value,sub_best = self.min_search(depth - 1, new_board,x,y,best_move)
            if value > v:
                v = value
                sub_best.append(((hori, vert),(tar_hori, tar_vert)))
                best = sub_best
            if v >= y:
                return v,[]
            x = max(x,v)
        for hori,vert in board.player_chess(self.type):
            posi_act = board.posi_act(self.type,hori,vert)
            for tar_hori,tar_vert in posi_act:
                new_board = deepcopy(board)
                NODE4 += 1
                if new_board.move(self.type,hori,vert,tar_hori,tar_vert):
                    cap = self.oppo
                value,sub_best = self.min_search(depth-1,new_board,x,y,[])
                if value > v:
                    v = value
                    sub_best.append(((hori, vert), (tar_hori, tar_vert)))
                    best = sub_best
                if v >= y:
                    return v,[]
                x = max(x, v)
        return v,best

    def min_search(self, depth, board: Board, x, y, best_move:list):
        if board.b_w == 0:
            if self.type == 'b':
                return self.def_eva1(board) + 400,[]
            else:
                return self.def_eva1(board) - 400,[]
        elif board.w_b == 0:
            if self.type == 'w':
                return self.def_eva1(board) + 400,[]
            else:
                return self.def_eva1(board) - 400,[]
        elif depth == 0:
            return self.def_eva1(board),[]
        cap = None
        v = MAX
        best =[]
        global NODE4
        if best_move:
            mov = best_move.pop()
            hori,vert = mov[0]
            tar_hori,tar_vert = mov[1]
            new_board = deepcopy(board)
            NODE4 += 1
            new_board.move(self.oppo, hori, vert, tar_hori, tar_vert)
            value,sub_best = self.max_search(depth - 1, new_board,x,y,best_move)
            if v > value:
                v = value
                sub_best.append(((hori,vert),(tar_hori,tar_vert)))
                best = sub_best
            if v <= x:
                return v,[]
            y = min(y,v)
        for hori, vert in board.player_chess(self.oppo):
            posi_act = board.posi_act(self.oppo, hori, vert)
            for tar_hori, tar_vert in posi_act:
                new_board = deepcopy(board)
                NODE4 += 1
                if new_board.move(self.oppo, hori, vert, tar_hori, tar_vert):
                    cap = self.type
                value, sub_best = self.max_search(depth - 1, new_board, x, y, [])
                if v > value:
                    v = value
                    sub_best.append(((hori, vert), (tar_hori, tar_vert)))
                    best = sub_best
                if v < x:
                    return v,[]
                y = min(y,v)
        return v,best

    def minimax_search(self, board:Board, max_depth=4):
        depth = 1
        best_move = []
        global NODE4
        while depth <= max_depth:
            cap = None
            x = MIN
            y = MAX
            v = MIN
            if best_move:
                best = best_move.pop()
                hori,vert = best[0]
                tar_hori,tar_vert = best[1]
                new_board = deepcopy(board)
                NODE4 += 1
                new_board.move(self.type,hori,vert,tar_hori,tar_vert)
                value,sub_best = self.min_search(depth-1,new_board,x,y,best_move)
                if value > v:
                    v = value
                    sub_best.append(((hori,vert),(tar_hori,tar_vert)))
                    best_move = sub_best
            for hori,vert in board.player_chess(self.type):
                posi_act = board.posi_act(self.type,hori,vert)
                for tar_hori,tar_vert in posi_act:
                    new_board = deepcopy(board)
                    NODE4 += 1
                    if new_board.move(self.type,hori,vert,tar_hori,tar_vert):
                        cap = self.oppo
                    value,sub_best = self.min_search(depth-1,new_board,x,y,[])
                    if v < value:
                        v = value
                        sub_best.append(((hori,vert),(tar_hori,tar_vert)))
                        best_move = sub_best
            depth += 1
        move = best_move.pop()
        return move