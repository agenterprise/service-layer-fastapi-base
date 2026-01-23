from typing import List

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.gen.domainmodel.aiapp import AbstractAiApp
from app.gen.domainmodel.router import AbstractRouter
from app.gen.middleware.http import BaseHttpMiddleware

class BaseAIApp(AbstractAiApp):
    
    def __init__(self, baserouters:List[AbstractRouter], middleware:BaseHttpMiddleware, **extra):
        super().__init__(openapi_url="/agent/api/openapi.json", **extra)   
        self.gen_middleware = middleware
        ## setup
        self.gen_middleware.define_middleware(app=self)
        for router in baserouters:
            router.define_routes()
            self.include_router(router.router)
        self.mount("/static", StaticFiles(directory="static"), name="static")

        @self.get("/docs/swagger", include_in_schema=False)
        async def custom_swagger_ui_html():
            return FileResponse("static/swagger/index.html")


        

        

    