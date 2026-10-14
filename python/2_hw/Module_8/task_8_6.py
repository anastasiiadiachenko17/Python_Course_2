"""Print all prime numbers between 1 and 50."""

SMALLEST_PRIME = 2
UPPER_LIMIT = 50

for number in range(SMALLEST_PRIME, UPPER_LIMIT + 1):
    is_prime = True

    for divisor in range(SMALLEST_PRIME, number):
        if number % divisor == 0:
            is_prime = False
            break

    if is_prime:
        print(number)
