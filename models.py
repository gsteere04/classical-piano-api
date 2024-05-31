from pydantic import BaseModel,Field
from typing import Optional

class Composer(BaseModel):
    name: str
    home_country: str

class Piece(BaseModel):
    name: str
    alt_name: str
    difficulty: int
    composer_id: int