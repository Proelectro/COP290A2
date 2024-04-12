#include <iostream>
#include <vector>
#include <utility>
#include <fstream>
#include <cstdlib>
using namespace std;

class DSU
{
public:
    int *parent;
    int *rank;
    int n;

    DSU(){

    };

    void init(int n)
    {
        this->n = n;
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++)
        {
            parent[i] = i;
            rank[i] = 0;
        }
    }

    ~DSU()
    {
        delete[] parent;
        delete[] rank;
    }

    int find(int x)
    {
        if (parent[x] == x)
            return x;
        return parent[x] = find(parent[x]);
    }

    void unite(int x, int y)
    {
        int s1 = find(x);
        int s2 = find(y);
        if (s1 != s2)
        {
            if (rank[s1] < rank[s2])
                parent[s1] = s2;
            else if (rank[s1] > rank[s2])
                parent[s2] = s1;
            else
            {
                parent[s1] = s2;
                rank[s2]++;
            }
        }
    }
};

class Maze
{
public:
    int n;
    int m;
    DSU dsu;
    vector<pair<int, int>> edges;
    vector<pair<int, int>> maze;
    ofstream fout;
    ofstream fout2;

    int start_x = 0;
    int start_y = 0;
    int end_x, end_y;

    Maze(int n, int m)
    {
        this->n = n;
        this->m = m;
        dsu.init(n * m);
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
            {
                if (i + 1 < n)
                    edges.push_back({i * m + j, (i + 1) * m + j});
                if (j + 1 < m)
                    edges.push_back({i * m + j, i * m + j + 1});
            }
        }
        // shuffle the edges in a random order
                srand(time(NULL));
        for (int i = 0; i < edges.size(); i++)
        {
            int j = rand() % edges.size();
            swap(edges[i], edges[j]);
        }
        // initialize fout to maze.txt
        fout.open("maze.txt");
        fout2.open("mazehist.txt");
        // start_x = rand() % m;
        // start_y = rand() % n;
        end_x = rand() % m;
        end_y = rand() % n;
    }

    void generate()
    {

        for (auto edge : edges)
        {
            int u = edge.first;
            int v = edge.second;
            if (dsu.find(u) != dsu.find(v))
            {
                dsu.unite(u, v);
                maze.push_back({u, v});
                print(false);
            }
        }
    }

    void print( bool boo)
    {
        vector<vector<char>> grid(2 * n + 1, vector<char>(2 * m + 1, '#'));
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
            {
                grid[2 * i + 1][2 * j + 1] = ' ';
            }
        }
        for (auto edge : maze)
        {
            int u = edge.first;
            int v = edge.second;
            int x1 = u / m;
            int y1 = u % m;
            int x2 = v / m;
            int y2 = v % m;
            if (x1 == x2)
            {
                grid[2 * x1 + 1][2 * min(y1, y2) + 2] = ' ';
            }
            else
            {
                grid[2 * min(x1, x2) + 2][2 * y1 + 1] = ' ';
            }
        }

        // pick a random start and end point

        grid[2 * start_x + 1][2 * start_y + 1] = 'S';
        grid[2 * end_x + 1][2 * end_y + 1] = 'G';

        // now write the grid to maze.txt

        for (int i = 0; i < 2 * n + 1; i++)
        {
            for (int j = 0; j < 2 * m + 1; j++)
            {
                (boo ? fout : fout2) << grid[i][j];
            }
            (boo ? fout : fout2) << endl;
        }

    }
};

int main()
{
    Maze maze(10, 10);
    maze.generate();
    maze.print(true);
    return 0;
}