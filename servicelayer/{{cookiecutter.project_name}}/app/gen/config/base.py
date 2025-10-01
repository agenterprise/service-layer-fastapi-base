from app.gen.config.settings import BaseAISettings, CrossCuttingSettings, LLMSettings, ToolSettings

class BaseEnvironmentContext():
    
    
    def AIAppBean(self,baserouters, middleware, title:str, version:str):
        from app.gen.aiapp import BaseAIApp
        return BaseAIApp(baserouters, middleware, title=title, version=version)

    def HttpMiddlewareBean(self):
        from app.gen.middleware.http import BaseHttpMiddleware as HttpMiddleware
        return HttpMiddleware()
    
   

    def ToolSettingsBean(self):
        return ToolSettings()   
    def LLMSettingsBean(self):
        return LLMSettings()
    def BaseAiSettingsBean(self):
        return BaseAISettings()
    def CrossCuttingSettingsBean(self):
        return CrossCuttingSettings()  

    """ Language Models""" 
    {% for key, llm in cookiecutter.llms.items() %}
    def {{llm.uid | aiurnvar | capitalize }}LLMBean(self):
        from app.gen.aimodel.{{llm.uid | aiurnimport}}.model import BaseLanguageModel as {{llm.uid | aiurnvar | capitalize}}
        return {{llm.uid | aiurnvar | capitalize}}(settings=self.LLMSettingsBean())
    {% endfor %}

    """ Agents """
    {% for key, agent in cookiecutter.agents.items() %}
    def {{agent.uid | aiurnvar | capitalize }}AgentBean(self):
        from app.gen.agents.{{agent.uid | aiurnimport}}.agent import BaseAgent as {{agent.uid | aiurnvar | capitalize}}
        llmmodel = self.{{agent.llmref | aiurnvar | capitalize}}LLMBean()
        
        return {{agent.uid | aiurnvar | capitalize}}(llmmodel=llmmodel,{% for ref in agent.toolrefs %}{{ref | aiurnvar}} = self.{{ref | aiurnvar | capitalize }}ToolBean(), {% endfor %})
    {% endfor %}

    """ Tools """
    {% for key, tool in cookiecutter.tools.items() %}
    def {{tool.uid | aiurnvar | capitalize }}ToolBean(self):
        from app.gen.tool.{{tool.uid | aiurnimport}}.tool import BaseTool as {{tool.uid | aiurnvar | capitalize}}
        return {{tool.uid | aiurnvar | capitalize}}(settings=self.ToolSettingsBean())
    {% endfor %}

    """ Router """
    def RouterBean(self,{% for key, agent in cookiecutter.agents.items() %}{{agent.uid | aiurnvar}}Agent,{% endfor %}):
        from app.gen.routes.router import BaseRouter as Router
        return Router({% for key, agent in cookiecutter.agents.items() %}{{agent.uid | aiurnvar}}={{agent.uid | aiurnvar}}Agent,{% endfor %})
    
    def app(self):
        """ Application instance """
        
        return self.AIAppBean(middleware=self.HttpMiddlewareBean(), 
                              baserouters=[self.RouterBean(self.CookAgentBean(),self.WaiterAgentBean())], 
                              title=self.BaseAiSettingsBean().app_name, 
                              version=self.BaseAiSettingsBean().app_version)

    def logger_conf(self):
        """ Logging configuration """
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
                "level": self.CrossCuttingSettingsBean().log_level,
                "handlers": ["default"],
                "propagate": False
            }
                }