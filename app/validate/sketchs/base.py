from pydantic import BaseModel, ConfigDict


class SketchsBasevalidate(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True, arbitrary_types_allowed=True)