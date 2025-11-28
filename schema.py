from pydantic import BaseModel

class DataSchema(BaseModel):
    """
        
    """

    time_taken: int
    day: str
    airline: str
    from_city: str
    to_city: str
    stops: str
    flight_class: str
    departure_time: str
    arrival_time: str