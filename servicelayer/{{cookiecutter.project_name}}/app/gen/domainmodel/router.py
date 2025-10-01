from pydantic import BaseModel
from app.gen.domainmodel.aiapp import AbstractAiApp
from app.gen.domainmodel.modelregistry import  BaseModelregistry

class AbstractRouter(BaseModel):

   def define_routes(self):
        pass