
from a2a.server.apps import A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore

from app.gen.config.settings import BaseAISettings, CrossCuttingSettings, LLMSettings, ToolSettings
from app.gen.domainmodel.a2a_agent_executor import A2AAgentExecutor

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
    {%- for key, llm in cookiecutter.llms.items() %}
    def {{llm.uid | aiurnvar | capitalize }}LLMBean(self):
        from app.gen.aimodel.{{llm.uid | aiurnimport}}.model import BaseLanguageModel as {{llm.uid | aiurnvar | capitalize}}
        return {{llm.uid | aiurnvar | capitalize}}(settings=self.LLMSettingsBean())
    {%- endfor %}

    """ Agents """
    {%- for key, agent in cookiecutter.agents.items() %}
    def {{agent.uid | aiurnvar | capitalize }}AgentBean(self):
        from app.gen.agents.{{agent.uid | aiurnimport}}.agent import BaseAgent as {{agent.uid | aiurnvar | capitalize}}
        llmmodel = self.{{agent.llmref | aiurnvar | capitalize}}LLMBean()
        
        return {{agent.uid | aiurnvar | capitalize}}(llmmodel=llmmodel,{%- for ref in agent.toolrefs %}{{ref | aiurnvar}} = self.{{ref | aiurnvar | capitalize }}ToolBean(),{%- endfor %} settings=self.BaseAiSettingsBean())
    {%- endfor %}

    """ Tools """
    {%- for key, tool in cookiecutter.tools.items() %}
    def {{tool.uid | aiurnvar | capitalize }}ToolBean(self):
        from app.gen.tool.{{tool.uid | aiurnimport}}.tool import BaseTool as {{tool.uid | aiurnvar | capitalize}}
        return {{tool.uid | aiurnvar | capitalize}}(settings=self.ToolSettingsBean())
    {%- endfor %}

    """ Router """
    def RouterBean(self,{%- for key, agent in cookiecutter.agents.items() %}{{agent.uid | aiurnvar}}Agent,{%- endfor %}):
        from app.gen.routes.router import BaseRouter as Router
        return Router({%- for key, agent in cookiecutter.agents.items() %}{{agent.uid | aiurnvar}}={{agent.uid | aiurnvar}}Agent,{%- endfor %})
    
    def a2a_app(self, app):
        agents = []
        {%- for key, agent in cookiecutter.agents.items() %}
        agents.append(self.{{agent.uid | aiurnvar | capitalize}}AgentBean())
        {%- endfor %}
        for agent in agents:
            request_handler = DefaultRequestHandler(
                agent_executor=A2AAgentExecutor(agent=agent),
                task_store=InMemoryTaskStore(),
            )
            server = A2AFastAPIApplication(
                agent_card=agent.get_agentcard(),
                http_handler=request_handler
            )
            app.mount(agent.a2a_path, app=server.build(redoc_url=None, docs_url=None))
        return app

    def app(self):
        """ Application instance """
        app =  self.AIAppBean(middleware=self.HttpMiddlewareBean(), 
                              baserouters=[self.RouterBean({%- for key, agent in cookiecutter.agents.items() %}self.{{agent.uid | aiurnvar | capitalize}}AgentBean(),{%- endfor %})], 
                              title=self.BaseAiSettingsBean().app_name, 
                              version=self.BaseAiSettingsBean().app_version)

        app = self.a2a_app(app)
        return app


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