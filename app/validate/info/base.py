from pydantic import BaseModel, ConfigDict
from datetime import datetime

class BaseInfoValid(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(extra='ignore', from_attributes=True, arbitrary_types_allowed=True)


