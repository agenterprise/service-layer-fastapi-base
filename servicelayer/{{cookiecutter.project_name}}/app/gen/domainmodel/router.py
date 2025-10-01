from pydantic import BaseModel
from app.gen.domainmodel.aiapp import AbstractAiApp

class AbstractRouter(BaseModel):

   def define_routes(self):
        pass