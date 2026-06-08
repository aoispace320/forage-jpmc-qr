import pandas as pd
import numpy as np

# ── Data ──────────────────────────────────────────────
df = pd.read_csv('../task three/loan_data.csv')

fico_data = df.groupby('fico_score').agg(
    n=('default', 'count'),
    k=('default', 'sum')
).reset_index()

scores = fico_data['fico_score'].values
n_arr  = fico_data['n'].values
k_arr  = fico_data['k'].values

# ── Cumulative sums for O(1) range queries ─────────────
cum_n = np.concatenate([[0], np.cumsum(n_arr)])
cum_k = np.concatenate([[0], np.cumsum(k_arr)])

# ── Log-likelihood for bucket [i, j] ──────────────────
def ll(i, j):
    n = cum_n[j+1] - cum_n[i]
    k = cum_k[j+1] - cum_k[i]
    if n == 0 or k == 0 or k == n:
        return -np.inf
    p = k / n
    return k * np.log(p) + (n - k) * np.log(1 - p)

# ── Dynamic Programming ────────────────────────────────
def dp_bucketing(num_buckets):
    m = len(scores)

    dp  = np.full((num_buckets + 1, m), -np.inf)
    ptr = np.zeros((num_buckets + 1, m), dtype=int)

    # base case: 1 bucket
    for j in range(m):
        dp[1][j] = ll(0, j)

    # fill DP table
    for b in range(2, num_buckets + 1):
        for j in range(b - 1, m):
            for i in range(b - 1, j + 1):
                val = dp[b-1][i-1] + ll(i, j)
                if val > dp[b][j]:
                    dp[b][j] = val
                    ptr[b][j] = i

    # backtrack to recover boundaries
    boundaries = []
    j = m - 1
    for b in range(num_buckets, 0, -1):
        boundaries.append(scores[j])
        j = ptr[b][j] - 1
    boundaries.append(scores[0])

    return sorted(boundaries)

# ── Rating map ─────────────────────────────────────────
def get_rating(fico, boundaries):
    """Lower rating = better credit (1 = best)"""
    for i, bound in enumerate(boundaries[1:], 1):
        if fico <= bound:
            return i
    return len(boundaries) - 1

# ── Run ────────────────────────────────────────────────
NUM_BUCKETS = 5
boundaries = dp_bucketing(NUM_BUCKETS)
print(f"Bucket boundaries: {boundaries}")

# show each bucket's default rate
print("\nBucket summary:")
for i in range(len(boundaries) - 1):
    lo, hi = boundaries[i], boundaries[i+1]
    bucket = df[(df['fico_score'] >= lo) & (df['fico_score'] <= hi)]
    n, k = len(bucket), bucket['default'].sum()
    print(f"  Rating {i+1}: FICO {lo}-{hi} | n={n}, defaults={k}, PD={k/n:.3f}")

# test
print("\nRating examples:")
for fico in [450, 550, 650, 720, 800]:
    print(f"  FICO {fico} → Rating {get_rating(fico, boundaries)}")