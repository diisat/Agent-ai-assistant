from fastapi import FastAPI
import math

app = FastAPI(title="Math API", description="Simple math functions as APIs")
@app.get("/add/{a}/{b}")
def add_numbers(a: float, b: float):
    """Add two numbers"""
    result = a + b
    return {"a": a, "b": b, "result": result}
@app.get("/multiply/{a}/{b}")
def multiply_numbers(a: float, b: float):
    """Multiply two numbers"""
    result = a * b
    return {"a": a, "b": b, "result": result}
@app.get("/square/{number}")
def square_number(number: float):
    """Calculate square of a number"""
    result = number ** 2
    return {"number": number, "square": result}
@app.get("/sqrt/{number}")
def square_root(number: float):
    """Calculate square root of a number"""
    if number < 0:
        return {"error": "Cannot calculate square root of negative number"}
    result = math.sqrt(number)
    return {"number": number, "square_root": result}