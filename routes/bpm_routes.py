from fastapi import APIRouter
from apis.bpm_api import conv_auto_model
from apis.bpm_api import forecasting_condition
from apis.bpm_api import emotional_stability_index
from pydantic import BaseModel
from typing import List

#class Bpm(BaseModel):
#    bpm:List[float]
    
router = APIRouter()

@router.post("/airesult")
async def results(bpm:list[float]):
    model=conv_auto_model()
    score, state=forecasting_condition(model,bpm)
    bpm_index, emotional_index=emotional_stability_index(bpm)
    return {"score":score,
            "state":state,
            "bpm_index":bpm_index,
            "emotional_index":emotional_index}
