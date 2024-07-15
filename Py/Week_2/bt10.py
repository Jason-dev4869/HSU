TAX = 0.07
TIP = 0.18

charge = float(input("Enter the charge for  the food: "))
tip_ammount = charge * TIP
tax_ammount = charge * TAX

total_cost = tax_ammount + tip_ammount + charge

print(f"VAT 7% is {tax_ammount:,.2f}")
print(f"Service tip 18% is {tip_ammount:,.2f}")
print(f"Total cost of the meal is {total_cost:,.2f}")