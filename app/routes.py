from fastapi import APIRouter
from app.schemas import TextInput
from app.services import predict_text

router = APIRouter()

@router.post("predict")
def predict(input: TextInput):
    return predict_text(input.text)