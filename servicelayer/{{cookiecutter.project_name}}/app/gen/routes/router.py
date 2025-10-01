import logging
from typing import ClassVar

from fastapi import Request
from app.gen.routes.health.handler import health as service_health
from app.gen.domainmodel.router import AbstractRouter
from app.gen.domainmodel.agent import  AbstractAgent

from fastapi import APIRouter

logger = logging.getLogger(__name__)

class BaseRouter(AbstractRouter):
   
    {% for key, agent in cookiecutter.agents.items() %}
    {{agent.uid | aiurnpath}}:AbstractAgent
    {% endfor %}

    router : ClassVar[APIRouter] = APIRouter()
    
    def define_routes(self):
        @self.router.get("/health",tags=["QoS"])
        async def handle_health(request: Request):
            return await service_health(request)
    
    
        {% for key, agent in cookiecutter.agents.items() %}
        @self.router.get("/agent/{{agent.name | lower | replace('"', '') }}/ask/{question}", tags=["agents"])
        async def handle_{{agent.uid | aiurnvar}}(request: Request, question):  
            return await self.{{agent.uid | aiurnpath}}.ask(question)
        {% endfor %}