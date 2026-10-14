"""Report whether the entered temperature means a hot day."""

HOT_THRESHOLD_C = 27

temperature = float(input("Enter the temperature in °C: "))

if temperature > HOT_THRESHOLD_C:
    print("It's a hot day.")
else:
    print("It's not a hot day.")
