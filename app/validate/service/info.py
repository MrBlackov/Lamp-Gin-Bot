from pydantic import BaseModel, ConfigDict
from app.validate.info.characters import CharacterInfo

class BaseServiceValidate(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class UserChars(BaseServiceValidate):
    chars: list[CharacterInfo] | None = None
    main_id: int | None = None
    no_chars: bool = False
    max_chars: int
    use_bonus: bool = False