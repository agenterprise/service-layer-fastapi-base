class IoCContainer:
    def __init__(self, modelregistry, toolregistry, router, middleware):
        self.modelregistry = modelregistry
        self.toolregistry = toolregistry
        self.router = router        
        self.middleware = middleware    