from . import mathematics
from . import economics
from . import text
from . import physics
from . import chemistry

from .text import *

__version__ = "0.1.0"
__author__ = "EduLib Developer"

__all__ = [
    "mathematics",
    "economics",
    "text",
    "physics",
    "chemistry",
    *text.__all__,
]