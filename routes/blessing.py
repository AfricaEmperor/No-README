
from fastapi import APIRouter, HTTPException, status
from models.blessing import Blessing
from typing import List

blessings = {}

router = APIRouter(
    prefix="/blessings",
    tags=["Blessings"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blessing(blessing: Blessing):
    if blessing.id in blessings:
        raise HTTPException(status_code=400, detail="Blessing ID already exists.")
    blessings[blessing.id] = blessing
    return {"message": "Blessing created successfully", "blessing": blessing}

@router.get("/", response_model=List[Blessing])
def list_blessings():
    return list(blessings.values())

@router.get("/{blessing_id}", response_model=Blessing)
def get_blessing(blessing_id: str):
    if blessing_id not in blessings:
        raise HTTPException(status_code=404, detail="Blessing not found.")
    return blessings[blessing_id]

@router.delete("/{blessing_id}", status_code=status.HTTP_200_OK)
def delete_blessing(blessing_id: str):
    if blessing_id not in blessings:
        raise HTTPException(status_code=404, detail="Blessing not found.")
    del blessings[blessing_id]
    return {"message": f"Blessing '{blessing_id}' deleted successfully"}
