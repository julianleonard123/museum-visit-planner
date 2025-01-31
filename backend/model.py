
from datetime import date
from pydantic import BaseModel
from typing import List, Optional

class Weather(BaseModel):
    forecast: Optional[List[str]]
    
class Venue(BaseModel):
    venueid: int
    name: Optional[str]
    fullname: Optional[str]
    city: Optional[str]
    state: Optional[str]
    
class Exhibition(BaseModel):
    id: int
    title: Optional[str]
    shortdescription: Optional[str]
    temporalorder:  Optional[int]
    venues: Optional[List[Venue]]
    weather: Optional[Weather] = None

