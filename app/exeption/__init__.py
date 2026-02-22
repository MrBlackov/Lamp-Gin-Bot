from .another import DiceError, AnotherError
from .api import ApiError, ValidationApiError
from .base import BotError, get_error_faq
from .item import EmodziNoValideError, ItemError, GiveItemNoEnterID, GiveItemNoEnterNameOrID, NameNoValideError, NotNameItemSketchError, SizeNotIntItemSketchError, ThrowAwayQuantityFloat, ThrowAwayQuantityLessOne, ThrowAwayQuantityMoreItemQuantity, ThrowAwayQuantityNoInt
from .service import ValidStrToJSONError, ValidToIntError, ValidToTypeError, ValidToStrError, ValidToStrLenError, ValidToIntPositiveError
from .transfer import TransferError, TransferNoFindError, TransferNoHaventItemError, TransferQuantityNoIntError, TransferSellerNoHaventItemError
from .char import CharError, CharHastNameError, BonusCharSubError, NoHaveMainChar
from .faq import FaqError, FaqErrorNoEnterError, FaqErrorNoFindError

error_faq: dict[str, BotError] = get_error_faq()
#print('\n'.join([f'{code}: {error}' for code, error in error_faq.items()]))