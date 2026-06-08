# Task 2: Natural Gas Storage Contract Pricing

## Objective
Build a prototype pricing model for a natural gas storage contract. The client wants to buy gas in summer, store it, and sell in winter to profit from seasonal price differentials. The model must generalize to multiple injection/withdrawal dates and account for all associated costs.

---

## Thought Process

### 1. Problem Framing
Any storage contract's value reduces to a simple cash flow identity:

$$\text{Contract Value} = \text{Revenue} - \text{Purchase Cost} - \text{Storage Cost} - \text{Injection/Withdrawal Cost}$$

The key insight is that this is a **deterministic valuation** given known (or estimated) future prices — not a stochastic derivatives pricing problem. We use the `get_price()` function from Task 1 to estimate prices at any date.

### 2. Cash Flow Components

| Component | Formula |
|---|---|
| Purchase cost | $\text{price}(t_{inj}) \times V_{inj}$ |
| Injection cost | $c_{inj} \times V_{inj}$ |
| Storage cost | $c_{storage} \times V_{held} \times \Delta t_{months}$ |
| Withdrawal revenue | $\text{price}(t_{with}) \times V_{with}$ |
| Withdrawal cost | $c_{with} \times V_{with}$ |

### 3. Volume Constraint
At every injection event, current volume plus injection rate must not exceed `max_volume`. Injections that would breach capacity are skipped with a warning — this enforces a hard physical constraint of the storage facility.

### 4. Storage Cost Calculation
Storage cost is computed over the full holding period: from the first injection date to the last withdrawal date, multiplied by the total volume held. This assumes the facility charges a flat monthly fee per unit of gas stored.

### 5. Interest Rate Assumption
Per the problem specification, interest rates are assumed zero. In a real pricing model, cash flows would be discounted to present value using an appropriate rate curve.

---

## Results

**Sample contract:**
- Inject: 500,000 MMBtu × 2 (Jun 2024, Jul 2024)
- Withdraw: 500,000 MMBtu × 2 (Dec 2024, Jan 2025)
- Storage cost: $0.10/MMBtu/month
- Injection/withdrawal cost: $0.01/MMBtu

```
Purchase cost:   -$11,530,000
Storage cost:      -$700,000
Sales revenue:  +$13,070,000
─────────────────────────────
Contract Value:    +$820,000
```

---

## Key Concepts
- **Cash flow decomposition**: breaking a contract into atomic cost/revenue events
- **Volume tracking**: enforcing physical storage constraints across multiple transactions
- **Price interpolation**: leveraging Task 1's `get_price()` for arbitrary date pricing
