from enum import Enum
from typing import Any, Callable
import logging
from pydantic import (
    AliasChoices,
    AmqpDsn,
    BaseModel,
    Field,
    ImportString,
    PostgresDsn,
    RedisDsn,
    IPvAnyAddress
)
from pydantic_settings import BaseSettings

class EnvEnum(str, Enum):
    base = 'base'
    dev = 'dev'
    uat = 'uat'
    int = 'int'
    prod = 'prod'
    unittest = 'unittest'
    systemtest = 'systemtest'
    loadtest = 'loadtest'


                      
class BaseAISettings(BaseSettings):
    run_environment: str = Field(EnvEnum.base, description="Environment the app is running in")  
    app_name:str = Field("AI-Environment {{cookiecutter.project_name}}", description="The name of the application")
    app_version:str = Field("0.1.0", description="The version of the application")
    uvicorn_host: IPvAnyAddress = Field("0.0.0.0", description="The host for Uvicorn to bind to")
    uvicorn_port: int = Field(9000, description="The port for Uvicorn to bind to")
    uvicorn_reload: bool = Field(True, description="Enable/disable Uvicorn auto-reload")
    uvicorn_log_level: str = Field("info", description="Logging level for Uvicorn")
    uvicorn_env_file: str = Field(".env", description="The env file to load environment variables from")
    log_format:str = Field("%(levelname)s: %(message)s")
    log_level:str = Field("INFO")

