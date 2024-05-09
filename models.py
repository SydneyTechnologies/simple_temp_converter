from pydantic import BaseModel

class Report(BaseModel):
    joke: str
    celsius: float
    fahrenheit: float
