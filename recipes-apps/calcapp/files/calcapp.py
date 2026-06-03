#!/usr/bin/python3

import math

VERSION = "3.0"

def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b
def power(a, b): return a ** b
def modulus(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a % b
def percentage(a, b): return (a * b) / 100
def square_root(a):
    if a < 0:
        return "Error: Cannot sqrt negative number"
    return math.sqrt(a)

history = []

print("=================================")
print(f"   SUBBU OS - Calculator v{VERSION}")
print("=================================")

while True:
    print("\nOperations:")
    print("  1.  Add")
    print("  2.  Subtract")
    print("  3.  Multiply")
    print("  4.  Divide")
    print("  5.  Power (a^b)")
    print("  6.  Modulus (a % b)")
    print("  7.  Percentage (a% of b)")
    print("  8.  Square Root (√a)")
    print("  9.  View History")
    print("  10. Clear History")
    print("  11. Exit")

    choice = input("\nEnter choice: ").strip()

    if choice == "11":
        print("Bye!")
        break

    elif choice == "9":
        if not history:
            print("\nNo history yet.")
        else:
            print("\n-- History --")
            for i, h in enumerate(history, 1):
                print(f"  {i}. {h}")
        continue

    elif choice == "10":
        history.clear()
        print("\nHistory cleared.")
        continue

    elif choice == "8":
        try:
            a = float(input("Enter number: "))
        except ValueError:
            print("Invalid number!")
            continue
        result = square_root(a)
        entry = f"√{a} = {result}"
        if "Error" not in str(result):
            history.append(entry)
        print(f"\n  Result: {result}")
        continue

    elif choice in ["1", "2", "3", "4", "5", "6", "7"]:
        try:
            a = float(input("Enter first number : "))
            b = float(input("Enter second number: "))
        except ValueError:
            print("Invalid number!")
            continue

        if choice == "1":
            result = add(a, b)
            entry = f"{a} + {b} = {result}"
        elif choice == "2":
            result = subtract(a, b)
            entry = f"{a} - {b} = {result}"
        elif choice == "3":
            result = multiply(a, b)
            entry = f"{a} * {b} = {result}"
        elif choice == "4":
            result = divide(a, b)
            entry = f"{a} / {b} = {result}"
        elif choice == "5":
            result = power(a, b)
            entry = f"{a} ^ {b} = {result}"
        elif choice == "6":
            result = modulus(a, b)
            entry = f"{a} % {b} = {result}"
        elif choice == "7":
            result = percentage(a, b)
            entry = f"{a}% of {b} = {result}"

        if "Error" not in str(result):
            history.append(entry)
        print(f"\n  Result: {result}")

    else:
        print("Invalid choice!")
