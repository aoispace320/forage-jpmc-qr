import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

# ── Data ──────────────────────────────────────────────
df = pd.read_csv('loan_data.csv')

FEATURES = ['credit_lines_outstanding', 'loan_amt_outstanding',
            'total_debt_outstanding', 'income',
            'years_employed', 'fico_score']

X = df[FEATURES]
y = df['default']

# ── Train / Test Split ────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Model ─────────────────────────────────────────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

# ── Evaluation ────────────────────────────────────────
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
print(f"AUC-ROC: {roc_auc_score(y_test, y_pred_proba):.4f}")
print(classification_report(y_test, model.predict(X_test_scaled)))

# ── Expected Loss Function ────────────────────────────
def expected_loss(credit_lines, loan_amt, total_debt,
                  income, years_employed, fico):
    """
    Returns (PD, Expected Loss)
    EL = PD x LGD x EAD
    LGD = 1 - recovery rate = 0.90
    EAD = loan_amt_outstanding
    """
    x = scaler.transform([[credit_lines, loan_amt, total_debt,
                           income, years_employed, fico]])
    pd_prob = model.predict_proba(x)[0][1]
    el = pd_prob * 0.90 * loan_amt
    return round(pd_prob, 4), round(el, 2)

# ── Test ──────────────────────────────────────────────
pd_val, el_val = expected_loss(
    credit_lines=0,
    loan_amt=10000,
    total_debt=3000,
    income=80000,
    years_employed=5,
    fico=720
)
print(f"PD: {pd_val},  Expected Loss: ${el_val}")