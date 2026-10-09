from datetime import date, timedelta

today = date.today()

deadline = date.today() - timedelta(days=1)

days_remaining = (deadline - today).days

print("Days remaining:", days_remaining)
if days_remaining < 0:
    print("OVERDUE")

elif days_remaining == 0:
    print("DUE TODAY")

elif days_remaining <= 7:
    print("DEADLINE APPROACHING")

else:
    print("NORMAL")