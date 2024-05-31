import json
from fastapi import FastAPI, HTTPException, status
from models import Composer, Piece
from typing import Optional

with open("composers.json", "r") as f:
    composers_list: list[dict] = json.load(f)


with open("pieces.json", "r") as f:
    piece_list: list[dict] = json.load(f)

#auto increments the composer id
def get_next_composer_id() -> int:
    if not composers_list:
        return 1
    return max(composer["composer_id"] for composer in composers_list) + 1

app = FastAPI()

@app.get("/")
async def get_composers():
    sorted_composers = sorted(composers_list, key=lambda x: x["composer_id"])
    return sorted_composers
#adds a composer to the list.  also checks for any gaps in the id numbers to ensure consistency.
@app.post("/composers", status_code=status.HTTP_201_CREATED)
async def create_composer(composer: Composer): 
    existing_ids = {composer["composer_id"] for composer in composers_list}
    
    # Find the lowest available ID
    new_composer_id = 1
    while new_composer_id in existing_ids:
        new_composer_id += 1

    # Add the new composer with the lowest available ID
    composer_data = composer.model_dump()
    composer_data["composer_id"] = new_composer_id
    composers_list.append(composer_data)

    return {"message": "Composer created successfully", "composer_id": new_composer_id}

@app.put("/composers/{composer_id}")
async def update_composer(composer_id: Optional[int], updated_composer: Composer) -> Composer:
    updated_composer_data = updated_composer.model_dump()

    if composer_id is not None:
        for i, composer in enumerate(composers_list):
            if composer["composer_id"] == composer_id:
                updated_composer_data["composer_id"] = composer_id
                composers_list[i] = updated_composer_data
                return updated_composer
        return {"message":"Composer not found"}, 404
    new_composer_id = get_next_composer_id()
    updated_composer_data["composer_id"] = new_composer_id
    composers_list.append(updated_composer_data)
    return {"message": "Composer created successfully", "composer_id": new_composer_id}

@app.delete("/composers/{composer_id}")
async def delete_composer(composer_id: Optional[int]):
    if composer_id is not None:
        for composer in composers_list:
            if composer["composer_id"] == composer_id:
                composers_list.remove(composer)
                return {"message": "Composer removed successfully"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Composer not found")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="composer_id is required for removing a composer")
