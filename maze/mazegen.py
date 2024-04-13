import random

class DSU:
    def __init__(self):
        self.parent = []
        self.rank = []
        self.n = 0

    def init(self, n):
        self.n = n
        self.parent = [i for i in range(n)]
        self.rank = [0 for i in range(n)]

    def find(self, x):
        if self.parent[x] == x:
            return x
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def unite(self, x, y):
        s1 = self.find(x)
        s2 = self.find(y)
        if s1 != s2:
            if self.rank[s1] < self.rank[s2]:
                self.parent[s1] = s2
            elif self.rank[s1] > self.rank[s2]:
                self.parent[s2] = s1
            else:
                self.parent[s1] = s2
                self.rank[s2] += 1

class Maze:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.dsu = DSU()
        self.edges = []
        self.maze = []
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.history = []
        self.dsu.init(n * m)
        for i in range(n):
            for j in range(m):
                if i + 1 < n:
                    self.edges.append((i * m + j, (i + 1) * m + j))
                if j + 1 < m:
                    self.edges.append((i * m + j, i * m + j + 1))

        random.seed()
        for i in range(len(self.edges)):
            j = random.randint(0, len(self.edges) - 1)
            self.edges[i], self.edges[j] = self.edges[j], self.edges[i]

        self.end_x = random.randint(0, m - 1)
        self.end_y = random.randint(0, n - 1)

    def __len__(self):
        return len(self.maze)
    def generate(self):
        for edge in self.edges:
            u, v = edge
            if self.dsu.find(u) != self.dsu.find(v):
                self.dsu.unite(u, v)
                self.maze.append((u, v))
                self.history.append(self.get())
        self.maze = self.history[-1]
        
    def __getitem__(self, idx):
        return self.maze[idx]

    def get(self):
        grid = [['#' for j in range(2 * self.m + 1)] for i in range(2 * self.n + 1)]
        for i in range(self.n):
            for j in range(self.m):
                grid[2 * i + 1][2 * j + 1] = ' '

        for edge in self.maze:
            u, v = edge
            x1 = u // self.m
            y1 = u % self.m
            x2 = v // self.m
            y2 = v % self.m
            if x1 == x2:
                grid[2 * x1 + 1][2 * min(y1, y2) + 2] = ' '
            else:
                grid[2 * min(x1, x2) + 2][2 * y1 + 1] = ' '
        return grid
    
if __name__ == "__main__":
    maze = Maze(4, 4)
    maze.generate()
    maze = maze.get()
    print("done")