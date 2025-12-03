from pydantic import BaseModel, ConfigDict

class OrmModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Photo(OrmModel):
    tg_id: int
    poster_id: int
    photo_id: str
    name: str