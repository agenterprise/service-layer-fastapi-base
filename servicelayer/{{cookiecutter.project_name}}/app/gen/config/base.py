from app.gen.config.service_settings import BaseAISettings
from app.gen.config.crosscutting_settings import CrossCuttingSettings

setting = BaseAISettings()
crosscutting = CrossCuttingSettings()

class BaseEnvironmentContext():
    
    from app.gen.domainmodel.modelregistry import BaseModelregistry
    from app.gen.domainmodel.toolregistry import BaseToolregistry


    def IoCContainerBean(self,
                      middleware, router, modelregistry, toolregistry):
        
        from app.gen.ioc.IoCContainer import IoCContainer
        return IoCContainer(
                middleware=middleware, 
                router=router, 
                modelregistry=modelregistry, 
                toolregistry=toolregistry)
    
    def AIAppBean(self,container, title:str, version:str):
        from app.gen.aiapp import BaseAIApp
        return BaseAIApp(iocContainer=container, title=title, version=version)

    def HttpMiddlewareBean(self):
        from app.gen.middleware.http import BaseHttpMiddleware as HttpMiddleware
        return HttpMiddleware()
    
    def ModelRegistryBean(self):
        from app.gen.aimodel.registry import baseAimodelregistry
        return baseAimodelregistry
    
    def ToolRegistryBean(self):
        from app.gen.tool.registry import baseToolregistry
        return baseToolregistry
    
    {% for key, llm in cookiecutter.llms.items() %}
    def {{llm.uid | aiurnvar | capitalize }}LLMBean(self):
        from app.gen.aimodel.{{llm.uid | aiurnimport}}.model import BaseLanguageModel as {{llm.uid | aiurnvar | capitalize}}
        return {{llm.uid | aiurnvar | capitalize}}()
    {% endfor %}

    {% for key, tool in cookiecutter.tools.items() %}
    def {{tool.uid | aiurnvar | capitalize }}ToolBean(self):
        from app.gen.tool.{{tool.uid | aiurnimport}}.tool import BaseTool as {{tool.uid | aiurnvar | capitalize}}
        return {{tool.uid | aiurnvar | capitalize}}()
    {% endfor %}

    {% for key, agent in cookiecutter.agents.items() %}
    def {{agent.uid | aiurnvar | capitalize }}AgentBean(self, modelregistry:BaseModelregistry=None, toolregistry:BaseToolregistry=None):
        from app.gen.agents.{{agent.uid | aiurnimport}}.agent import BaseAgent as {{agent.uid | aiurnvar | capitalize}}
        modelregistry = modelregistry or self.ModelRegistryBean()
        toolregistry = toolregistry or self.ToolRegistryBean()
        return {{agent.uid | aiurnvar | capitalize}}(modelregistry=modelregistry, toolregistry=toolregistry)
    {% endfor %}

    def RouterBean(self,{% for key, agent in cookiecutter.agents.items() %}{{agent.uid | aiurnvar}}Agent,{% endfor %}):
        from app.gen.routes.router import BaseRouter as Router
        return Router({% for key, agent in cookiecutter.agents.items() %}{{agent.uid | aiurnvar}}={{agent.uid | aiurnvar}}Agent,{% endfor %})
    
    def app(self):

        container = self.IoCContainerBean(
                middleware=self.HttpMiddlewareBean(), 
                router=self.RouterBean(self.CookAgentBean(),self.WaiterAgentBean()), 
                modelregistry=self.ModelRegistryBean(), 
                toolregistry=self.ToolRegistryBean())
        
        return self.AIAppBean(container, title=setting.app_name, version=setting.app_version)

    def logger_conf(self):
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "colorlog.ColoredFormatter",
                    "format": "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                },
                "access": {
                    "()": "colorlog.ColoredFormatter",
                    "format": "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr"
                },
                "access": {
                    "formatter": "access",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout"
                }
            },
            "loggers": {
                "uvicorn.error": {
                    "level": "INFO",
                    "handlers": ["default"],
                    "propagate": False
                },
                "uvicorn.access": {
                    "level": "INFO",
                    "handlers": ["access"],
                    "propagate": False
                }
            },
            "root": {
                "level": crosscutting.log_level,
                "handlers": ["default"],
                "propagate": False
            }
                }