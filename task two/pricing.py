import sys
sys.path.append('../task one')
from analysis import get_price
import pandas as pd
import numpy as np
from analysis import get_price  # Task 1 함수 가져오기

def price_contract(
    injection_dates,
    withdrawal_dates,
    injection_rate,      # MMBtu per injection
    max_volume,          # maximum storage capacity (MMBtu)
    storage_cost,        # cost per MMBtu per month
    inj_with_cost        # cost per MMBtu for injection/withdrawal
):
    current_volume = 0
    total_value = 0

    # injection (buying gas)
    for date in injection_dates:
        if current_volume + injection_rate > max_volume:
            print(f"WARNING: {date} - max volume exceeded, skipping")
            continue
        price = get_price(date)
        cost = price * injection_rate
        inj_cost = inj_with_cost * injection_rate
        current_volume += injection_rate
        total_value -= (cost + inj_cost)
        print(f"Inject {date}: price={price}, volume={injection_rate}, cost={cost:.2f}")

    # calculating storage cost
    start = pd.to_datetime(injection_dates[0])
    end = pd.to_datetime(withdrawal_dates[-1])
    months_stored = (end.year - start.year) * 12 + (end.month - start.month)
    storage_total = storage_cost * current_volume * months_stored
    total_value -= storage_total
    print(f"\nStorage: {months_stored} months, cost={storage_total:.2f}")

    # withdrawal (selling gas)
    for date in withdrawal_dates:
        if current_volume <= 0:
            print(f"WARNING: {date} - no gas left, skipping")
            continue
        price = get_price(date)
        revenue = price * injection_rate
        with_cost = inj_with_cost * injection_rate
        current_volume -= injection_rate
        total_value += (revenue - with_cost)
        print(f"Withdraw {date}: price={price}, volume={injection_rate}, revenue={revenue:.2f}")

    print(f"\nContract Value: ${total_value:.2f}")
    return total_value


# testing
price_contract(
    injection_dates=["2024-06-01", "2024-07-01"],
    withdrawal_dates=["2024-12-01", "2025-01-01"],
    injection_rate=500000,
    max_volume=1000000,
    storage_cost=0.1,
    inj_with_cost=0.01
)