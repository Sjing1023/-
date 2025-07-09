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