"""Report the age category for a person's age in years."""

MIN_AGE_SENIOR = 65
MIN_AGE_ADULT = 20
MIN_AGE_TEENAGER = 13
MIN_AGE_CHILD = 3

age = int(input("Enter the age in years: "))

if age >= MIN_AGE_SENIOR:
    category = "Senior"
elif age >= MIN_AGE_ADULT:
    category = "Adult"
elif age >= MIN_AGE_TEENAGER:
    category = "Teenager"
elif age >= MIN_AGE_CHILD:
    category = "Child"
else:
    category = "Infant"

print(f"Category: {category}")
