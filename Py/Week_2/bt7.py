TAX = 0.07
subtotal = 0

for i in range(1,6):
    price = float(input("Enter the  price of item {}: ".format(i)))
    subtotal += price

sale_tax = subtotal * TAX

total = sale_tax + subtotal

print(f"Subtotal of 5 item is {subtotal:,.2f} $")
print(f"VAT 7%  is {sale_tax:,.2f} $")
print(f"Total cost of items is {total:,.2f} $")