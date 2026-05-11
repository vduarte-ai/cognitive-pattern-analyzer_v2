from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.schemas import TextInput, PredictionOutput
from model.loader import classifier, embedding_model, label_encoder
from app.logger import logger
from app.services import analyze_text

router = APIRouter()

class TextRequest(BaseModel):
    text: str

@router.get("/")
def health():
    return {"status": "ok"}

@router.post("/predict", response_model=PredictionOutput)
def predict(request: TextInput):
    try:
        text = request.text

        if not text or len(text.strip()) == 0 :
            
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        result = analyze_text(text)

        return {
            "success": True,
            **result
        }
        
    except HTTPException:
        raise

    except Exception as e:

        logger.error(f"Prediction error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

        # 1. Convertir texto -> embedding 
        #embedding = embedding_model.encode([text])

        # 2. Clasifier
        #prediction = classifier.predict(embedding)
        #probabilities = classifier.predict_proba(embedding)

        # 3. Convertir a label
        #label = label_encoder.inverse_transform(prediction)[0]
        #confidence = float(max(probabilities[0]))
        
        #labels = label_encoder.classes_
        #probs = probabilities[0]

        #all_probs = {
        #    label: float(prob)
        #    for label, prob in zip(labels, probs)
        #}

        l#ogger.info(f"Incoming text: {text}")
        #logger.info(f"Prediction: {label}")       

        #return {
        #    "success": True,
        #    "prediction": label,
        #    "confidence": round(confidence, 3),
        #    "all_probabilities": all_probs
         #}
        
    #except Exception as e:
    #    logger.error(f"Prediction error: {str(e)}")

    #raise HTTPException(
    #    status_code=500,
    #    detail="Internal prediction error"
    #)