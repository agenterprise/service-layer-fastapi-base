from fastapi import FastAPI 

class AbstractAiApp(FastAPI):

   def __init__(self, **extra):
       super().__init__(**extra) 