def get_loan_and_upfront(price: float):
    loan = price * 0.80
    upfront = price * 0.07
    cash_needed = price * 0.20 + upfront
    return {"loan_amount": round(loan, 2), "upfront_costs": round(upfront, 2), "total_cash_needed": round(cash_needed, 2)}

def calculate_emi(loan_amount: float, years: int = 25) -> float:
    years = min(years, 25)
    r = 0.045 / 12
    n = years * 12
    emi = loan_amount * r * (1 + r)**n / ((1 + r)**n - 1)
    return round(emi, 2)

def calculate_amortization(loan_amount: float, years: int = 25):
    years = min(years, 25)
    emi = calculate_emi(loan_amount, years)
    r = 0.045 / 12
    balance = loan_amount
    schedule = []
    total_interest = 0
    for month in range(1, years * 12 + 1):
        interest = balance * r
        principal = emi - interest
        balance = max(balance - principal, 0)
        total_interest += interest
        schedule.append({
            "month": month,
            "payment": round(emi, 2),
            "principal": round(principal, 2),
            "interest": round(interest, 2),
            "balance": round(balance, 2)
        })
    return {
        "schedule": schedule,
        "total_interest": round(total_interest, 2),
        "total_paid": round(emi * years * 12, 2)
    }