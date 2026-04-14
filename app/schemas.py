from pydantic import BaseModel, Field

class TextInput(BaseModel):
    text: str = Field(..., min_length=3, max_length=500)

class PredictionOutput(BaseModel):
    prediction: str
    confidence: float