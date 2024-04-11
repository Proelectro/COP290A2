#include <iostream>
using namespace std;

class DSU
{
public:
    int *parent;
    int *rank;
    int n;

    DSU(int n)
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
    char **grid;
    DSU *dsu;

    Maze(int n, int m)
    {
        this->n = n;
        this->m = m;
        grid = new char *[n];
        for (int i = 0; i < n; i++)
        {
            grid[i] = new char[m];
            for (int j = 0; j < m; j++)
                grid[i][j] = '#';
        }
        dsu = new DSU(n * m);
    }

    

    void print()
    {
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
                cout << grid[i][j];
            cout << endl;
        }
    }
};

int main()
{
    int n, m;
    cin >> n >> m;
    Maze maze(n, m);
    maze.print();
    return 0;
}