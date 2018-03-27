import Chess
import timeit

board = Chess.Board()
off_player = Chess.OffPlayer2('w')
def_player = Chess.OffPlayer('b')
move1 = 0
move2 = 0
total1 = 0
total2 = 0
while True:
    start1 = timeit.default_timer()
    off_player.move(board)
    end1 = timeit.default_timer()
    total1 += (end1 - start1)
    move1 += 1
    if board.w_b == 0 or board.chess_num['b'] == 0:
        winner = 'player1'
        break
    start2 = timeit.default_timer()
    def_player.move(board)
    end2 = timeit.default_timer()
    total2 += (end2 - start2)
    move2 += 1
    if board.b_w == 0 or board.chess_num['w'] == 0:
        winner = 'player2'
        break
for i in board.board:
    print(i)
print('winner is',winner)
print('player1 expanded',Chess.NODE3,'nodes')
print('player2 expanded',Chess.NODE4,'nodes')
print('player1 expanded',Chess.NODE3/move1,'nodes per move')
print('player2 expanded',Chess.NODE4/move2,'nodes per move')
print('player1 uses',total1/move1,'s on average to make a move')
print('player2 uses',total2/move2,'s on average to make a move')
print('player1 captures',16-board.chess_num['b'],'workers')
print('player2 captures',16-board.chess_num['w'],'workers')