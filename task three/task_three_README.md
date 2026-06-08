# Task 3: Probability of Default and Expected Loss Model

## Objective
Given a loan book with borrower characteristics, build a model that estimates the probability of default (PD) for any borrower. Use PD to compute expected loss (EL) assuming a 10% recovery rate.

---

## Thought Process

### 1. Why Not Linear Regression?
The target variable `default` is binary (0 or 1). Linear regression produces unbounded outputs — predictions outside [0, 1] are meaningless as probabilities. A model that can output a "probability" of 1.4 has no interpretable meaning in a credit risk context.

### 2. Logistic Regression
Logistic regression maps any linear combination of features through a sigmoid function:

$$P(\text{default}) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + \cdots + \beta_p x_p)}}$$

This guarantees outputs in $(0, 1)$ and produces calibrated probabilities — the model's output directly represents likelihood of default.

**Why not Random Forest or XGBoost?**
In production credit risk models, interpretability is a regulatory requirement (Basel III/IV, IFRS 9). Regulators and model validation teams (e.g., MRGR) require that a model's decision can be explained for any individual borrower. Logistic regression's coefficients provide direct feature-level attribution. Black-box models require additional tooling (e.g., SHAP) and face higher scrutiny in model validation.

### 3. Feature Engineering
Beyond raw features, the example answer introduces ratio features that normalize by income:

```python
df['debt_to_income']    = df['total_debt_outstanding'] / df['income']
df['payment_to_income'] = df['loan_amt_outstanding']   / df['income']
```

A $50,000 debt means very different risk levels at $40,000 income vs $200,000 income. Ratios capture this relative burden, which is more predictive than absolute values. DTI (Debt-to-Income) is a standard metric in real-world credit underwriting.

### 4. Class Imbalance
The dataset has 81.5% non-default and 18.5% default observations. Accuracy alone is misleading — a naive model predicting "never default" achieves 81.5% accuracy. AUC-ROC is the appropriate metric: it measures the probability that the model assigns a higher risk score to a defaulting borrower than a non-defaulting one.

### 5. Data Leakage Observation
The model achieves AUC = 1.0, which is unrealistic in practice. Investigation reveals `credit_lines_outstanding` has near-perfect separation between classes (mean 0.74 for non-default vs 4.62 for default). This is a characteristic of synthetic data. In a real dataset, this would trigger a data leakage investigation before production deployment.

### 6. Expected Loss Formula

$$EL = PD \times LGD \times EAD$$

- **PD**: model output (predicted probability of default)
- **LGD**: Loss Given Default = $1 - \text{recovery rate} = 0.90$
- **EAD**: Exposure at Default = `loan_amt_outstanding`

---

## Results

```
High-risk borrower  (credit_lines=5, fico=580): PD=1.00, EL=$9,000
Low-risk borrower   (credit_lines=0, fico=720): PD=0.00, EL=$0
```

---

## Key Concepts
- **Logistic regression**: binary classification with calibrated probability output
- **Sigmoid function**: maps $\mathbb{R} \rightarrow (0,1)$
- **AUC-ROC**: discrimination metric robust to class imbalance
- **Expected Loss**: $EL = PD \times LGD \times EAD$
- **Feature engineering**: DTI and PTI ratios as domain-informed predictors
