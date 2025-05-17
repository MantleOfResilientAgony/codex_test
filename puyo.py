import random
import sys

WIDTH = 6
HEIGHT = 12
COLORS = ['R', 'G', 'B', 'Y', 'P']

class Piece:
    def __init__(self, colors, row, col, orientation=0):
        self.colors = colors  # [color0, color1]; color1 is pivot
        self.row = row
        self.col = col
        self.orientation = orientation  # 0 up, 1 right, 2 down, 3 left

    def cells(self):
        r, c = self.row, self.col
        if self.orientation == 0:  # color0 above pivot
            return [(r-1, c, self.colors[0]), (r, c, self.colors[1])]
        elif self.orientation == 1:  # color0 to right of pivot
            return [(r, c+1, self.colors[0]), (r, c, self.colors[1])]
        elif self.orientation == 2:  # color0 below pivot
            return [(r+1, c, self.colors[0]), (r, c, self.colors[1])]
        else:  # orientation == 3, color0 to left of pivot
            return [(r, c-1, self.colors[0]), (r, c, self.colors[1])]


def create_board():
    return [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]


def fits(board, piece):
    for r, c, _ in piece.cells():
        if c < 0 or c >= WIDTH or r >= HEIGHT:
            return False
        if r >= 0 and board[r][c] is not None:
            return False
    return True


def move(board, piece, dr, dc):
    new_piece = Piece(piece.colors, piece.row + dr, piece.col + dc, piece.orientation)
    if fits(board, new_piece):
        piece.row += dr
        piece.col += dc
        return True
    return False


def rotate(board, piece):
    new_piece = Piece(piece.colors, piece.row, piece.col, (piece.orientation + 1) % 4)
    if fits(board, new_piece):
        piece.orientation = new_piece.orientation
        return True
    # simple wall kick: try shifting left or right
    for dc in (-1, 1):
        shifted = Piece(piece.colors, piece.row, piece.col + dc, new_piece.orientation)
        if fits(board, shifted):
            piece.col += dc
            piece.orientation = new_piece.orientation
            return True
    return False


def place_piece(board, piece):
    for r, c, color in piece.cells():
        if r < 0:
            return False
        board[r][c] = color
    return True


def print_board(board, piece=None):
    temp = [row[:] for row in board]
    if piece is not None:
        for r, c, color in piece.cells():
            if 0 <= r < HEIGHT and 0 <= c < WIDTH:
                temp[r][c] = color.lower()
    print('+' + '-' * WIDTH + '+')
    for row in temp:
        line = ''.join(cell if cell is not None else ' ' for cell in row)
        print('|' + line + '|')
    print('+' + '-' * WIDTH + '+')


def clear_groups(board):
    removed = False
    visited = [[False]*WIDTH for _ in range(HEIGHT)]

    def bfs(sr, sc, color):
        stack = [(sr, sc)]
        group = []
        visited[sr][sc] = True
        while stack:
            r, c = stack.pop()
            group.append((r, c))
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r+dr, c+dc
                if 0<=nr<HEIGHT and 0<=nc<WIDTH and not visited[nr][nc] and board[nr][nc]==color:
                    visited[nr][nc] = True
                    stack.append((nr, nc))
        return group

    for r in range(HEIGHT):
        for c in range(WIDTH):
            color = board[r][c]
            if color is not None and not visited[r][c]:
                group = bfs(r, c, color)
                if len(group) >= 4:
                    for gr, gc in group:
                        board[gr][gc] = None
                    removed = True
    if removed:
        apply_gravity(board)
    return removed


def apply_gravity(board):
    for c in range(WIDTH):
        write_row = HEIGHT - 1
        for r in range(HEIGHT - 1, -1, -1):
            if board[r][c] is not None:
                if r != write_row:
                    board[write_row][c] = board[r][c]
                    board[r][c] = None
                write_row -= 1


def spawn_piece(board):
    colors = [random.choice(COLORS) for _ in range(2)]
    piece = Piece(colors, 1, WIDTH // 2)
    if not fits(board, piece):
        return None
    return piece


def main():
    board = create_board()
    piece = spawn_piece(board)
    if piece is None:
        print('Game Over')
        return
    while True:
        print_board(board, piece)
        cmd = input('Command (a left, d right, w rotate, s drop, q quit): ').strip()
        for ch in cmd:
            if ch == 'q':
                sys.exit()
            elif ch == 'a':
                move(board, piece, 0, -1)
            elif ch == 'd':
                move(board, piece, 0, 1)
            elif ch == 'w':
                rotate(board, piece)
            elif ch == 's':
                while move(board, piece, 1, 0):
                    pass
        if not move(board, piece, 1, 0):
            if not place_piece(board, piece):
                print_board(board)
                print('Game Over')
                break
            while clear_groups(board):
                pass
            piece = spawn_piece(board)
            if piece is None:
                print_board(board)
                print('Game Over')
                break

if __name__ == '__main__':
    main()
