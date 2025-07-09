import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random
import sys

class SlidePuzzleGame:
    def __init__(self, master, m, n, image_path):
        self.master = master
        self.m = m
        self.n = n
        self.image_path = image_path
        self.tiles = [] 
        self.tile_size = None
        self.board = []  
        self.goal = []  
        self.blank_pos = (m-1, n-1)
        self.images = []
        self.frame = None  
        self._load_image()
        self._init_board()
        self._draw_board()

    def _load_image(self):
        img = Image.open(self.image_path)
        w, h = img.size
        tile_w, tile_h = w // self.n, h // self.m
        self.tile_size = (tile_w, tile_h)
        self.tiles = []
        for i in range(self.m):
            for j in range(self.n):
                if i == self.m-1 and j == self.n-1:
                    continue  
                tile = img.crop((j*tile_w, i*tile_h, (j+1)*tile_w, (i+1)*tile_h))
                self.tiles.append(tile)

    def _init_board(self):
       
        self.goal = [[(i*self.n+j+1) % (self.m*self.n) for j in range(self.n)] for i in range(self.m)]
        
        nums = list(range(1, self.m*self.n)) + [0]
        while True:
            random.shuffle(nums)
            board = [nums[i*self.n:(i+1)*self.n] for i in range(self.m)]
            if self._is_solvable(board):
                break
        self.board = board
        for i in range(self.m):
            for j in range(self.n):
                if self.board[i][j] == 0:
                    self.blank_pos = (i, j)

    def _is_solvable(self, board):
        arr = sum(board, [])
        inv = 0
        arr_ = [x for x in arr if x != 0]
        for i in range(len(arr_)):
            for j in range(i+1, len(arr_)):
                if arr_[i] > arr_[j]:
                    inv += 1
        if self.n % 2 == 1:
            return inv % 2 == 0
        else:
            row = self.m - [row for row in board].index([x for x in board if 0 in x][0])
            return (inv + row) % 2 == 0

    def _draw_board(self):
        if hasattr(self, 'frame') and self.frame is not None:
            self.frame.destroy()
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.images = []
        for i in range(self.m):
            for j in range(self.n):
                idx = self.board[i][j]
                if idx == 0:
                    img = Image.new('RGB', self.tile_size, (255, 255, 255))
                else:
                    img = self.tiles[idx-1]
                tkimg = ImageTk.PhotoImage(img)
                self.images.append(tkimg)
                btn = tk.Button(self.frame, image=tkimg, command=lambda x=i, y=j: self._try_move(x, y))
                btn.grid(row=i, column=j)

    def _try_move(self, x, y):
        bx, by = self.blank_pos
        if (abs(bx-x) == 1 and by == y) or (abs(by-y) == 1 and bx == x):
            self.board[bx][by], self.board[x][y] = self.board[x][y], self.board[bx][by]
            self.blank_pos = (x, y)
            self._draw_board()
            if self._is_finished():
                messagebox.showinfo('恭喜', '拼图完成！')

    def _is_finished(self):
        for i in range(self.m):
            for j in range(self.n):
                if self.board[i][j] != self.goal[i][j]:
                    return False
        return True

def main():
    print('滑动拼图游戏')
    m = int(input('请输入行数m：'))
    n = int(input('请输入列数n：'))
    print('请选择图片文件...')
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title='选择图片', filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.bmp')])
    if not file_path:
        print('未选择图片，程序退出')
        sys.exit(0)
    root.deiconify()
    root.title('滑动拼图游戏')
    game = SlidePuzzleGame(root, m, n, file_path)
    root.mainloop()

if __name__ == '__main__':
    main() 