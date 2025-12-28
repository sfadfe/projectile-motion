N, M, V = map(int, input().split())
a = [[0] * (N+1) for _ in range(N+1)]
for i in range(M):
    u, v = map(int, input().split())
    a[u][v] = 1
    a[v][u] = 1

visited = [False] * (N+1)

def DFS(v):
    visited[v] = True
    print(v, end=' ')
    for i in range(1, N+1):
        if a[v][i] == 1 and not visited[i]:
            DFS(i)
DFS(V)