# -
滑动谜题通解与滑动拼图游戏
B1：研究通用滑动谜题算法：参照教材6.2.4节的滑动谜题问题，研究实现通用m x n格板的滑动谜题解题程序。 
B2：通用滑动谜题演示：通用m x n滑动谜题，依次固定时间间隔或键盘手控步进演示解题步骤。
B3：滑动拼图游戏应用：用户输入m, n, 及一个图片文件名，将图片分割成m x n个小方块，以此替代B2中的数字，通过与特定块(0号)的位置交换，逐渐完成由杂乱图片到正确拼出原始图片的拼图过程。

1.1选题基本内容
研究实现通用 m x n 格板的滑动谜题解题程序，能够解决不同尺寸格板的滑动谜题问题。​
实现通用 m x n 滑动谜题的演示功能，支持依次固定时间间隔或键盘手控步进演示解题步骤。​
开发滑动拼图游戏应用，用户输入 m、n 及图片文件名后，能将图片分割成 m x n 个小方块，通过与特定块（0 号）的位置交换完成拼图过程

1.2开发环境介绍
 使用Python 3.10.9 环境，可使用pip包管理器安装项目所需的依赖库，如用于图形界面开发的Tkinter（Python 自带），用于图片处理的Pillow等。该版本具有诸多特性，如结构模式匹配，可使代码在处理滑动谜题不同状态的逻辑判断时更加简洁清晰；错误提示的改进能帮助开发者快速定位和解决代码中的问题；在性能上也有一定优化，能提高算法的运行效率，满足项目中对滑动谜题求解和演示的需求。
Tkinter：Python 自带的图形用户界面开发库，无需额外安装。在项目中用于构建滑动谜题的演示界面和滑动拼图游戏的交互界面，通过其提供的组件（如按钮、标签、画布等），可以方便地实现格板的显示、方块的移动以及用户交互操作。​
Pillow：用于图片处理的库，支持多种图片格式的读取、分割、缩放等操作。在滑动拼图游戏中，使用该库将用户输入的图片分割成 m×n 个小方块，并对图片块进行显示和处理，确保图片块的正确分割和显示。


2算法研究
2.1问题描述
通过实现通用 m x n 格板的滑动谜题解题程序，能够解决不同尺寸格板的滑动谜题问题。​
实现通用 m x n 滑动谜题的演示功能，支持依次固定时间间隔或键盘手控步进演示解题步骤。​
开发滑动拼图游戏应用，用户输入 m、n 及图片文件名后，能将图片分割成 m x n 个小方块，通过与特定块（0 号）的位置交换完成拼图过程

2.2设计思路
1.核心算法层：负责实现通用滑动谜题的解题算法，包括状态表示、可解性判断、搜索策略（BFS/DFS/A*）等，为整个系统提供解题能力。
2.演示交互层：基于核心算法层的结果，实现固定时间间隔或键盘手控的解题步骤演示，以及用户交互的拼图游戏界面。
3.图片处理层：专门处理用户输入的图片，实现图片分割、块替换等功能，将数字滑动谜题转化为图片滑动拼图。
二、核心算法设计
状态表示与操作
使用二维数组表示格板状态，例如 3x3 格板初始状态可表示为[[1,2,3],[4,0,5],[7,8,6]]
实现状态转换函数，根据 0 的位置生成所有可能的移动状态

2.3程序目录及核心代码

import heapq
from typing import List, Tuple, Optional

class SlidePuzzleSolver:
    def __init__(self, start: List[List[int]], goal: List[List[int]]):
        self.start = start
        self.goal = goal
        self.m = len(start)
        self.n = len(start[0])
        self.goal_pos = self._get_goal_positions(goal)

    def _get_goal_positions(self, goal: List[List[int]]) -> dict:
        pos = {}
        for i in range(self.m):
            for j in range(self.n):
                pos[goal[i][j]] = (i, j)
        return pos

    def _manhattan(self, state: Tuple[Tuple[int, ...], ...]) -> int:
        dist = 0
        for i in range(self.m):
            for j in range(self.n):
                val = state[i][j]
                if val == 0:
                    continue
                gi, gj = self.goal_pos[val]
                dist += abs(i - gi) + abs(j - gj)
        return dist

    def _find_zero(self, state: Tuple[Tuple[int, ...], ...]) -> Tuple[int, int]:
        for i in range(self.m):
            for j in range(self.n):
                if state[i][j] == 0:
                    return i, j
        return -1, -1

    def _get_neighbors(self, state: Tuple[Tuple[int, ...], ...]) -> List[Tuple[Tuple[Tuple[int, ...], ...], str, int]]:
        neighbors = []
        x, y = self._find_zero(state)
        directions = [(-1,0,'上'), (1,0,'下'), (0,-1,'左'), (0,1,'右')]
        for dx, dy, move in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.m and 0 <= ny < self.n:
                new_state = [list(row) for row in state]
                moved_num = new_state[nx][ny]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                neighbors.append((tuple(tuple(row) for row in new_state), move, moved_num))
        return neighbors

    def solve(self) -> Optional[List[str]]:
        start_state = tuple(tuple(row) for row in self.start)
        goal_state = tuple(tuple(row) for row in self.goal)
        heap = []
        heapq.heappush(heap, (self._manhattan(start_state), 0, start_state, []))
        visited = set()
        while heap:
            f, g, state, path = heapq.heappop(heap)
            if state == goal_state:
                return path
            if state in visited:
                continue
            visited.add(state)
            for neighbor, move, moved_num in self._get_neighbors(state):
                if neighbor not in visited:
                    step_desc = f"将数字{moved_num}向{move}移动"
                    heapq.heappush(heap, (g+1+self._manhattan(neighbor), g+1, neighbor, path+[step_desc]))
        return None

def input_board(m: int, n: int, prompt: str) -> List[List[int]]:
    print(prompt)
    board = []
    for i in range(m):
        row = list(map(int, input(f"第{i+1}行（用空格分隔）：").split()))
        assert len(row) == n, "每行输入的数字个数必须等于列数"
        board.append(row)
    return board

def main():
    print("通用滑动谜题求解器（支持任意m x n）")
    m = int(input("请输入行数m："))
    n = int(input("请输入列数n："))
    start = input_board(m, n, "请输入初始状态（0表示空格）：")
    goal = input_board(m, n, "请输入目标状态：")
    solver = SlidePuzzleSolver(start, goal)
    result = solver.solve()
    if result is None:
        print("无解！")
    else:
        print(f"最少步数：{len(result)}")
        print("移动步骤：")
        for i, step in enumerate(result, 1):
            print(f"第{i}步：{step}")

if __name__ == "__main__":
    main() 


2.4测试与结果

2.5分析与结论
成功实现了通用滑动谜题的 A * 求解器，具有良好的算法设计和代码结构。对于中小规模的谜题（如 3×3、3×4）能够高效求解，并提供清晰的解题步骤。然而，在处理大规模谜题时，内存和时间开销会显著增加。通过进一步优化算法和增强功能，可以提升其在更复杂场景下的实用性。
3测试对比(或应用原型，或功能扩展)
3.1问题描述
在实现滑动谜题通用求解器的基础上，需要对不同算法性能进行对比分析，验证求解器在不同场景下的有效性通过剪枝策略减少无效搜索，提高效率，对于实时性要求高的场景，可考虑使用神经网络预训练启发式函数，通过在终端输入1/2进行自发性测试或者进行手动一步一步讲滑动谜题解决。

3.2设计思路
滑动拼图求解器采用了 A * 搜索算法来找到从初始状态到目标状态的最短路径，实现通用 m x n 滑动谜题的演示功能，支持依次固定时间间隔或键盘手控步进演示解题步骤。
3.3程序目录及核心代码

3.4测试与结果




3.5分析与结论
时间复杂度：
A * 算法的时间复杂度理论上是指数级的，最坏情况下为 O (b^d)，其中 b 是分支因子（每个状态的平均可能移动数），d 是解的深度。
对于 3x3 拼图，分支因子约为 3（空格在中间时有 4 个移动，边缘有 3 个，角落有 2 个）。
实际性能取决于启发式函数的有效性，曼哈顿距离大大减少了搜索空间。
空间复杂度：
主要由优先队列和已访问集合的大小决定。
空间复杂度同样是指数级的，最坏情况下为 O (b^d)。
在实际求解复杂问题时，可能需要大量内存。
可扩展性：
该实现支持任意 m×n 的棋盘尺寸。
随着棋盘尺寸增大，状态空间呈指数级增长。
4x4 及以上的拼图可能需要较长时间或更多内存。

4 算法应用
4.1 问题描述
开发滑动拼图游戏应用，用户输入 m、n 及图片文件名后，能将图片分割成 m x n 个小方块，通过与特定块（0 号）的位置交换完成拼图过程。
4.2设计思路
界面设计：

使用 Tkinter 创建了简洁的图形界面
图片被分割成 m×n 个小方块，最后一个位置为空格
每个方块作为按钮，点击时尝试移动到空格位置

核心功能：

图片加载与分割：将用户选择的图片分割成 m×n 个小方块
随机生成初始状态：确保生成的拼图是可解的
移动逻辑：点击方块时，检查是否可以移动到空格位置
胜利条件判断：检查当前状态是否与目标状态一致

算法实现：

可解性判断：根据拼图大小和逆序数判断随机生成的状态是否可解
状态表示：使用二维数组表示拼图状态
移动逻辑：通过交换空格与相邻方块实现移动

4.3程序目录及核心代码
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

4.4测试与结果



4.5分析与结论
通过随机打乱数字序列生成初始状态，但严格通过可解性判断算法筛选有效状态，避免出现无解拼图。
可解性判断依据：
对于奇数列拼图：逆序数为偶数则可解；
对于偶数列拼图：逆序数与空格所在行数之和为偶数则可解。
这一设计确保了玩家始终能通过合理移动完成拼图，避免无效尝试。
