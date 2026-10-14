"""Keep asking for a password until the correct one is entered."""

CORRECT_PASSWORD = "qwerty"

while True:
    password = input("Enter the password: ")
    if password == CORRECT_PASSWORD:
        break
    print("Wrong password. Try again.")

print("Access granted.")
