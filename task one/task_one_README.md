# Task 1: Natural Gas Price Estimation

## Objective
Given monthly natural gas price data (Oct 2020 – Sep 2024), build a model that estimates the purchase price of gas at any given date — including extrapolation one year into the future.

---

## Thought Process

### 1. Exploratory Analysis
Started by visualizing the raw time series. Two patterns were immediately apparent:
- A long-term **upward trend** in price levels
- A recurring **seasonal cycle** with peaks in winter and troughs in summer

This suggested a decomposition approach: model trend and seasonality separately, then combine.

### 2. Why Not Linear Regression Alone?
A simple linear model captures trend but ignores seasonality. Residuals would show a clear periodic structure, violating the assumption of random error.

### 3. Model Design: Trend + Fourier Seasonality
Chose a regression model of the form:

$$\text{Price}(t) = \beta_0 + \beta_1 t + \beta_2 \sin\left(\frac{2\pi t}{12}\right) + \beta_3 \cos\left(\frac{2\pi t}{12}\right)$$

Where $t$ is a monthly time index starting at 0.

**Why sin + cos together?**
Using only $\sin$ fixes the phase of the seasonal peak. Combining both terms is equivalent to:

$$R \sin\left(\frac{2\pi t}{12} + \phi\right)$$

where $R = \sqrt{\beta_2^2 + \beta_3^2}$ (amplitude) and $\phi = \arctan(\beta_3 / \beta_2)$ (phase shift). The regression learns both the magnitude and the timing of the seasonal peak from the data.

**Why not monthly dummy variables?**
Dummy variables fix the seasonal pattern to the training window. Sin/cos terms extrapolate naturally — mathematically extending the wave beyond the observed data — which is essential for a pricing model that needs to forecast future dates.

### 4. Fitted Coefficients

| Parameter | Value | Interpretation |
|---|---|---|
| $\beta_0$ | 10.13 | Base price at $t=0$ |
| $\beta_1$ | 0.046 | ~$0.046/month long-run trend |
| $\beta_2$ | 0.690 | Seasonal amplitude |
| $\beta_3$ | -0.038 | Phase shift (peak ≈ January) |

Amplitude $R \approx 0.69$, consistent with observed winter/summer price spread.

### 5. Extrapolation
Extended the feature matrix 12 months beyond the last observation. The model smoothly continues both the trend and seasonal wave.

---

## Results

```
get_price("2024-06-15") → $11.56   # summer trough
get_price("2025-03-31") → $12.93   # winter peak
```

---

## Key Concepts
- **Time series decomposition**: trend + seasonality + residual
- **Fourier features**: encoding periodicity via sin/cos for smooth extrapolation
- **Phase-amplitude representation**: $A\sin + B\cos \equiv R\sin(\cdot + \phi)$
