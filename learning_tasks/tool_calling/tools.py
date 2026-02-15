from datetime import datetime


def calculator(a: float, b: float, operation: str):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    else:
        raise ValueError("Invalid operation")


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")
