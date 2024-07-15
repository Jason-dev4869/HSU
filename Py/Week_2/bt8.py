purchase = float(input("Enter the ammount of purchase: "))
num_instalments = int(input("Enter the desired number of instalments: "))

total_purchase = purchase * 1.05

instalments_ammount = total_purchase / num_instalments

print(f"The total purchase is {total_purchase:,.2f} $")
print(f"Each instalment will cost: {instalments_ammount:,.2f} $")