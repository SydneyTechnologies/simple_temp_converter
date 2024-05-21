from pydantic import BaseModel

class Report(BaseModel):
    joke: str
    celsius: float
    fahrenheit: float


class WsbData(BaseModel):
    websiteTitle: str
    gmbKey: str
    concept: str
    country: str = ""
    city: str = ""
    aboutKeywords: str = ""
    language: str = "en_gb"
    defaultColor: str = "rustic"
    pronouns: str = "We"
    optionSet: list = []
    additionalData: dict = {}

    # constants
    submitCount: int = 1
    addShopSection: bool = False

