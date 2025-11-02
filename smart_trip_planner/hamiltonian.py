import itertools
import numpy as np


# Given selected_df (pandas) return route as list of destination names in optimal visiting order,
# total distance, and the distance matrix used (aligned with route order)


def _make_distance_matrix(n, seed=7):
rng = np.random.default_rng(seed)
mat = rng.integers(50, 500, size=(n, n))
for i in range(n):
mat[i, i] = 0
for j in range(i+1, n):
mat[j, i] = mat[i, j]
return mat




def find_best_route(selected_df):
if selected_df.empty:
return [], 0, []
cities = list(selected_df['Destination'])
n = len(cities)
dist = _make_distance_matrix(n)


best_perm = None
best_cost = float('inf')
# brute-force permutations (suitable for small n <= 9)
for perm in itertools.permutations(range(n)):
cost = 0
for i in range(n - 1):
cost += dist[perm[i], perm[i+1]]
# optional: close cycle (return to start) -> include dist[perm[-1], perm[0]]
cost += dist[perm[-1], perm[0]]
if cost < best_cost:
best_cost = cost
best_perm = perm


route = [cities[i] for i in best_perm]
# reorder dist matrix to match route order for plotting convenience
ordered_idx = list(best_perm)
ordered_dist = dist[np.ix_(ordered_idx, ordered_idx)].tolist()
return route, int(best_cost), ordered_dist