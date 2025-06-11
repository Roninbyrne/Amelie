from Amelie.core.dir import dirr
from Amelie.core.bot import app
from Amelie.core.bot import start_bot

from .logging import LOGGER

dirr()

__all__ = ["app", "start_bot"]