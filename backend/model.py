
from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class Weather(BaseModel):
    city: str = Optional[str]
    temperature: Optional[float]
    humidity: Optional[float]
    
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
    # startDate: Optional[date]
    # endDate: Optional[date] 
    venues: Optional[List[Venue]]
    # weather: Optional[Weather]

