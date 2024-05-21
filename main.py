import re
import os
import logging
from models import Report, WsbData
from fastapi import FastAPI, Request, Query, Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
logging.basicConfig(level=logging.DEBUG)


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


@app.get("/image")
def get_temp_image(request: Request, value: float, temp_type: str, render: bool = False):
    image_location = ""
    if (temp_type.lower() == "f"):
        if value >= 80:
            image_location = "hot.webp"
        elif value > 60 and value < 80:
            image_location = "medium.webp"
        elif value <= 60:
            image_location = "cold.webp"
    else:
        if value >= 35:
            image_location = "hot.webp"
        elif value > 20 and value < 35:
            image_location = "medium.webp"
        elif value <= 20:
            image_location = "cold.webp"

    base_url = request.base_url
    image_url= f"{base_url}static/images/{image_location}"
    if render:
        return RedirectResponse(image_url)
    else:
        return {"image": image_url}
    

@app.get("/get_report")
def get_report(request: Request, joke: str, celsius: float, fahrenheit: float):
    url = request.base_url
    joke = joke.replace(" ", "%20")
    report_url = f"{url}report?joke={joke}&celsius={celsius}&fahrenheit={fahrenheit}"
    return {"report_url": report_url}



@app.get("/report", response_class=HTMLResponse)
def get_report(request: Request, joke: str, celsius: float, fahrenheit: float):
    joke = joke.replace("%20", " ")
    data = Report(joke=joke, celsius=celsius, fahrenheit=fahrenheit)
    return templates.TemplateResponse(request=request, name="sample.html", context=data.__dict__)


@app.post("/test")
def test(request: Request, data: WsbData ):
    previewLink = f"{request.base_url}static/images/preview.png"
    gptResponse = {
        "sitePreviewUrl": previewLink, 
        "trialSignUpUrl": "https://www.one.com/en/",
    }
    return gptResponse