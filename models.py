from pydantic import BaseModel

class Report(BaseModel):
    joke: str
    image: str
    celsius: float
    fahrenheit: float
