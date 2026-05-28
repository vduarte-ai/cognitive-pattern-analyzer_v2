from pydantic import BaseModel, Field

class TextInput(BaseModel):
    text: str = Field(..., min_length=3, max_length=500)

class PredictionOutput(BaseModel):
    success: bool
    prediction: str
    confidence: float
    confidence_label: str 
    all_probabilities: dict
    explanation: str
    reframing: str
    emotion: str
    companion_response: str
    

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
    
class UserLogin(BaseModel):
    email: str
    password: str
