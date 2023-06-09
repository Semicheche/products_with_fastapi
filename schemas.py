from pydantic import BaseModel
import datetime

class Products(BaseModel):
    title: str
    description: str
    at_sale: bool = False
    inventory: int
