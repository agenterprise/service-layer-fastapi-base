from typing import List
from app.gen.domainmodel.aiapp import AbstractAiApp
from app.gen.domainmodel.router import AbstractRouter
from app.gen.middleware.http import BaseHttpMiddleware

class BaseAIApp(AbstractAiApp):
    
    def __init__(self, baserouters:List[AbstractRouter], middleware:BaseHttpMiddleware, **extra):
        super().__init__(**extra)   
        self.gen_middleware = middleware
        ## setup
        self.gen_middleware.define_middleware(app=self)
        for router in baserouters:
            router.define_routes()
            self.include_router(router.router)

        


    