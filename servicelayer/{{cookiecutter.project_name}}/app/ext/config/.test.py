from app.gen.config.settings import BaseAISettings, CrossCuttingSettings
from app.gen.config.base import BaseEnvironmentContext as BaseEnvironmentContext   

setting = BaseAISettings()
crosscutting = CrossCuttingSettings()

class SystemTestEnvironmentContext(BaseEnvironmentContext):
    pass   

class LoadTestEnvironmentContext(BaseEnvironmentContext):
    pass   


 