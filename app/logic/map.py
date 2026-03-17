import igraph as ig
import matplotlib.pyplot as plt

# 1. Создаем граф с 5 вершинами и заданными ребрами
n_vertices = 5
edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (3, 4)]
g = ig.Graph(n_vertices, edges)

# 2. Добавляем атрибуты (имена, пол, семейное положение)
g.vs["name"] = ["Даниил", "Катя", "Кай", "Джошуа", "Яна"]
g.vs["gender"] = ["M", "F", "F", "M", "F"]
g.es["married"] = [False, False, False, True, False, False, False, True]

# Меняем атрибут конкретного ребра (поженились)
g.es[0]["married"] = True

# 3. Визуализируем
fig, ax = plt.subplots(figsize=(5,5))
ig.plot(
    g,
    target=ax,
    vertex_color=["steelblue" if gen == "M" else "salmon" for gen in g.vs["gender"]],
    vertex_label=g.vs["name"],
    edge_width=[2 if married else 1 for married in g.es["married"]],
    edge_color=["red" if married else "grey" for married in g.es["married"]]
)
plt.show()