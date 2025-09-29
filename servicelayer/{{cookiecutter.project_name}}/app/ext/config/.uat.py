from app.gen.config.service_settings import BaseAISettings
from app.gen.config.crosscutting_settings import CrossCuttingSettings
from app.gen.config.base import BaseEnvironmentContext as BaseEnvironmentContext   

setting = BaseAISettings()
crosscutting = CrossCuttingSettings()

class DevContext(BaseEnvironmentContext):
    pass   
   

 