from enum import Enum
from typing import Any, Callable
from pydantic import (

    Field,

)
from pydantic_settings import BaseSettings

                      
class CrossCuttingSettings(BaseSettings):
    log_format:str = Field("%(asctime)s %(levelname)s: %(message)s")
    log_level:str = Field("INFO")

