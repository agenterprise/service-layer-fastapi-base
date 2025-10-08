import logging
from typing import ClassVar, List

from fastapi import Request
from app.gen.routes.health.handler import health as service_health
from app.gen.domainmodel.router import AbstractRouter
from app.gen.domainmodel.agent import  AbstractAgent

 {%- for key, agent in cookiecutter.agents.items() %}
{%- if agent.input %}
from app.gen.entities.{{agent.input | aiurnimport }}.entity import {{agent.input | aiurnvar | capitalize }}Entity as {{agent.uid | aiurnvar | capitalize}}RequestModel
{%- else %}
from app.gen.domainmodel.baseentity import BaseInputEntity as {{agent.uid | aiurnvar | capitalize}}RequestModel
{%-endif%}

{%- if agent.output %}
from app.gen.entities.{{agent.output | aiurnimport }}.entity import {{agent.output | aiurnvar | capitalize }}Entity as {{agent.uid | aiurnvar| capitalize}}ResponseModel
{%- else %}
from app.gen.domainmodel.baseentity import BaseOutputEntity as {{agent.uid | aiurnvar | capitalize}}ResponseModel
{%-endif%}
{%- endfor %}
from fastapi import APIRouter

logger = logging.getLogger(__name__)

class BaseRouter(AbstractRouter):
   
    {%- for key, agent in cookiecutter.agents.items() %}
    {{agent.uid | aiurnpath}}:AbstractAgent
    {%- endfor %}

    router : ClassVar[APIRouter] = APIRouter()
    
    def define_routes(self):
        @self.router.get("/health",tags=["QoS"])
        async def handle_health(request: Request):
            return await service_health(request)
    
    
        {%- for key, agent in cookiecutter.agents.items() %}
        @self.router.post("/agent/{{agent.name | lower | replace('"', '') }}/ask", tags=["agents"],response_model={{agent.uid | aiurnvar | capitalize}}ResponseModel)
        async def handle_{{agent.uid | aiurnvar}}(request: Request, query:{{agent.uid | aiurnvar | capitalize}}RequestModel):  
            return await self.{{agent.uid | aiurnpath}}.ask(query)
        {%- endfor %}