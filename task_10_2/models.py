
from pydantic import BaseModel, conint, confloat, constr
from typing import Optional

class Cat(BaseModel):
    name: constr(min_length=2, max_length=50)
    age: conint(gt=0, lt=30)
    breed: constr(min_length=2, max_length=50)
    color: constr(min_length=2, max_length=50)
    weight: confloat(ge=0.0)
    vaccinated: bool
    special_needs: Optional[str] = None
    description: Optional[str] = 'Cute cat is finding home'