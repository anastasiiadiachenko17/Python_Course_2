"""Report whether a positive integer is a prime number."""

SMALLEST_PRIME = 2

number = int(input("Enter a positive integer: "))

is_prime = number >= SMALLEST_PRIME
divisor = SMALLEST_PRIME

while divisor * divisor <= number:
    if number % divisor == 0:
        is_prime = False
        break
    divisor += 1

if is_prime:
    print(f"{number} is a prime number.")
else:
    print(f"{number} is not a prime number.")
