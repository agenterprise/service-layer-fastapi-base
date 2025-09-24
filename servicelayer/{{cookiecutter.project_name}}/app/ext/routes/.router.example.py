from pydantic import BaseModel
from app.gen.routes.router import BaseRouter
class Router(BaseRouter):
    
    def define_routes(self):
        # do my stuff here
        super().define_routes() 