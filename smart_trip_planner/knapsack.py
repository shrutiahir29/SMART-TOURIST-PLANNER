import math
import pandas as pd


# Discretized knapsack: convert cost to units to keep DP feasible in browser/server
# unit = 100 means cost 3000 → 30 units


def knapsack_select(df: pd.DataFrame, total_budget: int, total_days: float, unit: int = 100):
# make working copy
items = df.copy().reset_index(drop=True)
items['CostUnit'] = (items['Cost'] / unit).apply(lambda x: max(1, int(round(x))))
# time in half-days as integer (0.5 -> 1)
items['TimeUnit'] = (items['TimeRequired'] * 2).apply(lambda x: max(1, int(round(x))))
B = int(total_budget // unit)
T = int(total_days * 2)
n = len(items)


# DP table: dp[b][t] = max popularity
dp = [[0] * (T + 1) for _ in range(B + 1)]
# parent pointer: store index chosen at state
parent = [[None] * (T + 1) for _ in range(B + 1)]


for i in range(n):
cost = items.at[i, 'CostUnit']
time = items.at[i, 'TimeUnit']
val = int(items.at[i, 'Popularity'])
# iterate backwards
for b in range(B, cost - 1, -1):
for t in range(T, time - 1, -1):
candidate = dp[b - cost][t - time] + val
if candidate > dp[b][t]:
dp[b][t] = candidate
parent[b][t] = i


# backtrack
b, t = B, T
chosen_idx = set()
while b > 0 and t > 0 and parent[b][t] is not None:
i = parent[b][t]
if i in chosen_idx:
break
chosen_idx.add(i)
b -= items.at[i, 'CostUnit']
t -= items.at[i, 'TimeUnit']


if not chosen_idx:
return pd.DataFrame(columns=df.columns)


selected = items.loc[sorted(list(chosen_idx))].copy()
# convert back to original columns
selected = selected[df.columns]
return selected