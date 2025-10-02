import uvicorn
import traceback
import logging
from app.gen.config.settings import BaseAISettings, EnvEnum, CrossCuttingSettings


settings = BaseAISettings()
crosscutting = CrossCuttingSettings()
logger = logging.getLogger(__name__)


def app():
    try:
              
        logger.info(f"Running App in Env Mode: {settings.run_environment}")
        return __get_context().app()
    except Exception as e:
        logger.critical(f"Error during app initialization: {e}")
        logger.error(traceback.format_exc())
        raise

def __get_context():
    if settings.run_environment == EnvEnum.base:
        from app.gen.config.base import BaseEnvironmentContext as Context
    if settings.run_environment == EnvEnum.dev:
        from app.ext.config.dev import DevelopmentEnvironmentContext as Context
    if settings.run_environment == EnvEnum.uat:
        from app.ext.config.uat import UserAcceptanceEnvironmentContext as Context
    if settings.run_environment == EnvEnum.int:
        from app.ext.config.int import IntegationEnvironmentContext as Context
    if settings.run_environment == EnvEnum.loadtest:
        from app.ext.config.test import LoadTestEnvironmentContext as Context
    if settings.run_environment == EnvEnum.systemtest:
        from app.ext.config.test import SystemTestEnvironmentContext as Context
    if settings.run_environment == EnvEnum.prod:
        from app.ext.config.prod import ProductionEnvironmentContext as Context
    if settings.run_environment == EnvEnum.ref:
        from app.ext.config.prod import ReferenceEnvironmentContext as Context
    
    return Context()

def logger_conf():
    try:
        logger.info(f"Applying Logging in Env Mode: {settings.run_environment}")
        return __get_context().logger_conf()
    except Exception as e:
        logger.critical(f"Error during logger initialization: {e}")
        logger.error(traceback.format_exc())
        raise

def main():
    logger.info(f"Starting {settings.app_name}")
    uvicorn.run("main:app", 
                host=str(settings.uvicorn_host), 
                reload=settings.uvicorn_reload, 
                port=settings.uvicorn_port, 
                env_file=settings.uvicorn_env_file, 
                log_level=settings.uvicorn_log_level,
                log_config=logger_conf(),
                factory=True)
if __name__ == "__main__":
    main()