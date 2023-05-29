from pydantic import BaseModel


class Holiday(BaseModel):
    title: str
    day: int
    month: int
