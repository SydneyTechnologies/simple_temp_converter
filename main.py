import re
import os
import logging
from models import Report, WsbData
from fastapi import FastAPI, Request, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from uuid import uuid4


static_dir = os.path.join(os.path.dirname(__file__), "static")
app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory="templates")
logging.basicConfig(level=logging.DEBUG)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}

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


@app.post("/build")
def test(request: Request, data: WsbData ):

    mapping  = {
    "cafe": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/Cafe.png",
    "membership": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/Membership.png",
    "portfolio": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/Portfolio.png",
    "beauty": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/beauty.png",
    "businessProf": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/businessProf.png",
    "coaches": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/coaches.png",
    "commercialrecreation": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/commercialRecreation.png",
    "creativeProf": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/creativeProf.png",
    "events": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/events.png",
    "health": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/health.png",
    "hotels": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/hotels.png",
    "musician": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/musician.png",
    "personalWebsite": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/personalWebsite.png",
    "publicAreas": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/publicAreas.png",
    "restaurants": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/restaurants.png",
    "serviceProf": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/serviceProf.png",
    "shops": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/shops.png",
    "bars": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/EE.png",
    "servicesCatchall": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/EE.png",
    "projects": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/EE.png",
    "projectsCatchall": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/EE.png",
    "nonProfit": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/EE.png",
    "organizationCatchall": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/EE.png",
    "eventCatchall": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/EE.png",
    "onlineShopCatchall": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/EE.png",
    "physicalStoreCatchall": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/EE.png",
    "portfolioCatchall": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/EE.png",
    "personalWebsiteCatchall": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/EE.png",
    "commercialRecreation": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/EE.png",
    "suppliers": "https://raw.githubusercontent.com/adakidpv/WSB-Templates-Trial/main/EE.png"
}
    



    previewLink = mapping.get(data.concept)
    session_id = str(uuid4())
    gptResponse = {
        "sitePreviewUrl": previewLink, 
        "trialSignUpUrl": f"https://try-websitebuilder.one.com/?session-id={session_id}",
    }
    return gptResponse