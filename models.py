from pydantic import BaseModel

class Report(BaseModel):
    joke: str
    celsius: float
    fahrenheit: float


class WsbData(BaseModel):
    websiteTitle: str = "Mandy's Website"
    country: str = ""
    city: str = ""
    gmbKey: str 
    group: bool = True
    concept: str 
    aboutKeywords: str

    # Optional fields
    optionSet: list = []
    submitCount: int = 1
    defaultColor: dict = {
        "accentColor": [
            "HSL",
            0.01486199575371549,
            0.6460905349794239,
            0.5235294117647059,
            1
        ],
        "mainColor": [
            "HSL",
            0,
            0,
            0.9725490196078431,
            1
        ],
        "whiteColor": [
            "HSL",
            0,
            0,
            1,
            1
        ],
        "blackColor": [
            "HSL",
            0.5645,
            0,
            0.23529411764705882,
            1
        ]
    }
    addressData: dict = {}
    language: str = "en_gb"
    additionalData: dict 
    addShopSection: bool = False

 