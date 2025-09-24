import uvicorn
import traceback
import logging
from app.gen.config.service_settings import BaseAISettings, EnvEnum
from app.gen.config.crosscutting_settings import CrossCuttingSettings

settings = BaseAISettings()
logger = logging.getLogger(__name__)
crosscutting = CrossCuttingSettings()
def app():
   
    try:
        if settings.run_environment == EnvEnum.base:
            from app.gen.config.base import BaseEnvironmentContext as Context
        if settings.run_environment == EnvEnum.dev:
            from app.ext.config.dev import DevContext as Context

        logger.info(f"Running App in Env Mode: {settings.run_environment}")
        return Context().app()
    except Exception as e:
        logger.critical(f"Error during app initialization: {e}")
        logger.error(traceback.format_exc())
        raise

def logger_conf():
    try:
        if settings.run_environment == EnvEnum.base:
            from app.gen.config.base import BaseEnvironmentContext as Context
        if settings.run_environment == EnvEnum.dev:
            from app.ext.config.dev import DevContext as Context


        logger.info(f"Applying Logging in Env Mode: {settings.run_environment}")
        return Context().logger_conf()
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