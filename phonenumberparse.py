import phonenumbers

number = "+91 9146196969"
x = phonenumbers.parse(number, None)
print(x.national_number)
