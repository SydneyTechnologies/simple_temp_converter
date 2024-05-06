import re
from fastapi import FastAPI

app = FastAPI()


def get_value(input: str):
    regex = r"([0-9]+)([a-zA-Z]+)"
    match = re.match(regex, input)
    if match:
        value = match.groups()[0]
        return value
    else:
        return None

@app.get("/temperature")
def read_temperature(input: str):
    try:
        value = get_value(input)
        if "f" in input.lower():
            return {"type": "F", "value": float(value)}
        elif 'c' in input.lower():
            return {"type": "C", "value": float(value)}
        else:
            return {"type": "UNKNOWN", "value": float(value)}
    except:
        return {"type": "UNKNOWN", "value": None}


@app.get("/tofahrenheit")
def convert_to_fahrenheit(value: float):
    return {"result": (value * 9/5) + 32}


@app.get("/tocelsius")
def convert_to_celsius(value: float):
    return {"result": (value - 32) * 5/9}


