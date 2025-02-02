
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

class Poster(BaseModel):
    imageurl: Optional[str]
    
class Exhibition(BaseModel):
    id: int
    title: Optional[str]
    begindate: Optional[date]
    enddate: Optional[date]
    shortdescription: Optional[str]
    temporalorder:  Optional[int]
    venues: Optional[List[Venue]]
    poster: Optional[Poster] = None
    weather: Optional[Weather] = None

