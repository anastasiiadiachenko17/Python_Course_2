"""Report the letter grade for a numerical score."""

MIN_SCORE_A = 90
MIN_SCORE_B = 80
MIN_SCORE_C = 70
MIN_SCORE_D = 60

score = float(input("Enter the score (0-100): "))

if score >= MIN_SCORE_A:
    grade = "A"
elif score >= MIN_SCORE_B:
    grade = "B"
elif score >= MIN_SCORE_C:
    grade = "C"
elif score >= MIN_SCORE_D:
    grade = "D"
else:
    grade = "F"

print(f"Grade: {grade}")
