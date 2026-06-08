# Task 4: FICO Score Bucketing via Dynamic Programming

## Objective
Map continuous FICO scores (300–850) into a fixed number of discrete rating buckets, where each bucket is assigned a rating (1 = best credit, n = worst). The bucketing must optimize the log-likelihood of observed default rates, making the buckets maximally informative for predicting PD.

---

## Thought Process

### 1. Why Bucketing?
Certain ML architectures require categorical inputs. Rather than applying uniform or arbitrary quantiles, we want buckets that reflect the actual default behavior of borrowers — each bucket should represent a meaningfully distinct risk tier.

### 2. Optimization Criterion: Log-Likelihood
Two candidate objectives were considered:

**MSE**: Minimizes approximation error of the FICO scores themselves. Treats this as a signal compression problem with no reference to default behavior.

**Log-likelihood**: Maximizes the statistical likelihood of observing the actual default outcomes given the bucket structure:

$$LL = \sum_{i=1}^{r} \left[ k_i \ln p_i + (n_i - k_i) \ln(1 - p_i) \right]$$

Where $p_i = k_i / n_i$ is the empirical default rate in bucket $i$.

Log-likelihood was chosen because the goal is **predictive discrimination**, not signal fidelity. Buckets with homogeneous default rates maximize LL — the model is penalized for mixing high-risk and low-risk borrowers in the same bucket.

### 3. Why Dynamic Programming?
Exhaustive search over all possible bucket boundaries is combinatorially intractable. For $m$ unique FICO scores and $r$ buckets, the number of ways to place $r-1$ boundaries is $\binom{m-1}{r-1}$. For $m=374, r=5$, this is over $10^9$ combinations.

DP exploits **optimal substructure**: the optimal $r$-bucket solution for scores $[0, j]$ can be built from the optimal $(r-1)$-bucket solution for scores $[0, i]$ plus one additional bucket $[i+1, j]$.

### 4. Recurrence

Define:
$$dp[b][j] = \text{maximum LL for scores } [0, j] \text{ split into } b \text{ buckets}$$

Recurrence:
$$dp[b][j] = \max_{i < j} \left( dp[b-1][i-1] + LL(i, j) \right)$$

Base case:
$$dp[1][j] = LL(0, j)$$

A pointer array `ptr[b][j]` stores the optimal split index at each state, enabling boundary recovery via backtracking.

### 5. O(1) Range Queries
Computing $LL(i, j)$ requires $n_{ij}$ and $k_{ij}$ — total customers and defaults in $[i, j]$. Using prefix sums:

$$n_{ij} = \text{cum\_n}[j+1] - \text{cum\_n}[i]$$
$$k_{ij} = \text{cum\_k}[j+1] - \text{cum\_k}[i]$$

This reduces each LL evaluation from $O(n)$ to $O(1)$, making the overall DP feasible.

### 6. Edge Cases
When $k=0$ or $k=n$ (bucket has zero defaults or all defaults), $\ln(0)$ is undefined. These states return $-\infty$, effectively preventing the optimizer from placing boundaries there.

---

## Results (5 buckets)

| Rating | FICO Range | Customers | Defaults | PD |
|---|---|---|---|---|
| 1 (best) | 696 – 850 | 1,683 | 79 | 4.7% |
| 2 | 640 – 696 | 3,253 | 345 | 10.6% |
| 3 | 580 – 640 | 3,481 | 716 | 20.6% |
| 4 | 520 – 580 | 1,417 | 543 | 38.3% |
| 5 (worst) | 408 – 520 | 301 | 199 | 66.1% |

PD decreases monotonically across ratings — the bucketing correctly orders credit risk.

---

## Key Concepts
- **Quantization**: mapping continuous values to discrete categories
- **Log-likelihood**: measures how well a probabilistic model explains observed outcomes
- **Dynamic programming**: solving optimization via overlapping subproblems
- **Optimal substructure**: $r$-bucket solution built incrementally from $(r-1)$-bucket solutions
- **Prefix sums**: $O(1)$ range aggregation for efficient DP transitions
